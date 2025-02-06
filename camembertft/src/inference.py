import torch
import config
import dataset
from model import NERModel
from config import Config

# Load configuration
config = Config()

def map_to_general_labels(labels):
    """
    Maps fine-grained labels to general labels [O, PER, LOC, ORG, MISC].
    - O : Non-entity
    - PER : Person
    - LOC : Location
    - ORG : Organization
    - MISC : Miscellaneous entity
    """
    general_map = {
        0: 0,  # O -> O
        1: 1, 2: 1,  # B-PER, I-PER -> PER
        3: 2, 4: 2,  # B-LOC, I-LOC -> LOC
        5: 3, 6: 3,  # B-ORG, I-ORG -> ORG
        7: 4, 8: 4   # B-MISC, I-MISC -> MISC
    }
    # Use .get() to avoid errors for unknown labels
    return [general_map.get(label, label) for label in labels]

def process_ner_predictions(tokenized_sentence, model, test_dataset, enc_tag_inv):
    """
    Performs named entity recognition (NER) predictions and returns the words and their extracted entities.
    """
    # Move the model and data to the appropriate device (GPU if available)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Perform predictions on the data
    all_preds = []
    with torch.no_grad():
        data = test_dataset[0]
        for k, v in data.items():
            data[k] = v.to(device).unsqueeze(0)  # Add batch dimension

        tag, _ = model(**data)

        # Extract predictions as labels
        preds = tag.argmax(dim=2).cpu().numpy().reshape(-1)
        all_preds.extend(preds)

    # Map entities to general categories
    general_preds = map_to_general_labels(all_preds)

    # Extract entities based on predictions
    extracted_entities = [enc_tag_inv.get(item, 'O') for item in general_preds][1:len(tokenized_sentence)-1]

    # Align tokens with their corresponding entities
    aligned_tokens = []
    word_idx = 0
    for token, pred in zip(tokenized_sentence[1:len(tokenized_sentence)-1], extracted_entities):
        # Ensure all sub-tokens receive the same label as the first sub-token of the word
        if token.startswith("▁"):  # If it's a sub-token, it belongs to the previous word
            aligned_tokens.append((token, pred))  # Add the token and its label
        else:
            # Update the previous token's label
            aligned_tokens[-1] = (aligned_tokens[-1][0] + token, aligned_tokens[-1][1])

    # Clean extracted words by removing the "▁" prefix
    words = [word.replace("▁", "") for word, _ in aligned_tokens]
    entities = [str(entity).split("-")[1] if len(str(entity).split("-")) == 2 else entity for _, entity in aligned_tokens]

    return words, entities

if __name__ == "__main__":
    # Initialize variables and parameters
    enc_tag = config.CLASSES
    enc_tag_inv = {v: k for k, v in enc_tag.items()}
    num_tag = config.NUM_TAG

    sentence = """
    oui bonjour madame Alice, il va aux urgences à 8 rue le pieux, Ici c'est Paris
    """
    
    # Tokenize the sentence
    tokenized_sentence = config.TOKENIZER.encode(sentence)
    tokens = config.TOKENIZER.convert_ids_to_tokens(tokenized_sentence)

    # Create a dataset for prediction
    sentence_split = sentence.split()
    test_dataset = dataset.CustomDataset(
        texts=[sentence_split],  
        tags=[[0] * len(sentence_split)]  # No real tags are provided for testing
    )

    # Load the model and make predictions
    model = NERModel(num_tag=num_tag)
    model.load_state_dict(torch.load(config.MODEL_PATH, map_location='cpu', weights_only=True))

    words, entities = process_ner_predictions(tokens, model, test_dataset, enc_tag_inv)

    # Display extracted entities and their positions
    print("\nExtracted entities:")
    print(f"words: {words}")
    print(f"entities: {entities}")