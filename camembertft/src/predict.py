import numpy as np
import joblib
import torch
from sklearn.metrics import classification_report
import json
import config
import dataset
from model import NERModel
from train import process_data
import time
from config import Config

# Load configuration
config = Config()

def map_to_general_labels(labels):
    """
    Map fine-grained labels to general labels [O, PER, LOC, ORG, MISC].
    - O: Non-entity
    - PER: Person
    - LOC: Location
    - ORG: Organization
    - MISC: Miscellaneous entity
    """
    general_map = {
        0: 0,  # O -> O
        1: 1, 2: 1,  # B-PER, I-PER -> PER
        3: 2, 4: 2,  # B-LOC, I-LOC -> LOC
        5: 3, 6: 3,  # B-ORG, I-ORG -> ORG
        7: 4, 8: 4   # B-MISC, I-MISC -> MISC
    }
    return [general_map[label] for label in labels]

if __name__ == "__main__":
    # Load encoding tags and number of tags from configuration
    enc_tag = config.CLASSES
    num_tag = config.NUM_TAG

    # Load and process test data
    sentences, tags, enc_tag = process_data(config.TRAINING_FILE)
    test_dataset = dataset.CustomDataset(texts=sentences, tags=tags)
    test_data_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=1, num_workers=4
    )

    # Set device (GPU if available, otherwise CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load the pre-trained NER model
    model = NERModel(num_tag=num_tag)
    model.load_state_dict(torch.load(config.MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()  # Set the model to evaluation mode

    # Initialize lists to store predictions and targets
    all_preds = []
    all_targets = []

    # Perform inference on the test dataset
    with torch.no_grad():
        for batch in test_data_loader:
            # Move batch data to the appropriate device
            inputs = {key: val.to(device) for key, val in batch.items()}
            targets = batch["target_tags"].to(device)

            # Get model predictions
            outputs, _ = model(**inputs)
            preds = outputs.argmax(2)  # Take the index of the most likely class

            # Flatten predictions and targets, and filter out ignored labels (-100)
            active_preds = preds.view(-1)
            active_targets = targets.view(-1)

            valid_idx = active_targets != -100  # Identify valid labels
            all_preds.extend(active_preds[valid_idx].cpu().numpy())  # Store valid predictions
            all_targets.extend(active_targets[valid_idx].cpu().numpy())  # Store valid targets

    # Generate a detailed classification report for all classes
    target_names = list(enc_tag.keys())
    detailed_report = classification_report(
        all_targets, all_preds, target_names=target_names, output_dict=True
    )

    # Map fine-grained labels to general categories
    general_targets = map_to_general_labels(all_targets)
    general_preds = map_to_general_labels(all_preds)

    # Generate a classification report for general categories
    general_target_names = ["O", "PER", "LOC", "ORG", "MISC"]
    general_report = classification_report(
        general_targets, general_preds, target_names=general_target_names, output_dict=True
    )

    # Export detailed and general reports to JSON files
    with open(config.RESULT_DETAIL_PATH, "w") as f:
        json.dump(detailed_report, f, indent=4)

    with open(config.RESULT_GENERAL_PATH, "w") as f:
        json.dump(general_report, f, indent=4)

    print("Reports exported: detailed_report.json and general_report.json")