import numpy as np
import joblib
import torch
from sklearn.metrics import classification_report
import json
import config
import dataset
from model import EntityModel
from train import process_data
import time
def map_to_general_labels(labels):
    """
    Map fine-grained labels to general labels [O, PER, LOC, ORG, MISC].
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
    
    enc_tag = config.CLASSES
    num_tag = config.NUM_TAG

    # Charger les données de test
    sentences, tags, enc_tag = process_data(config.TRAINING_FILE)
    test_dataset = dataset.CustomDataset(texts=sentences, tags=tags)
    test_data_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=1, num_workers=4
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = EntityModel(num_tag=num_tag)
    model.load_state_dict(torch.load(config.MODEL_PATH, map_location=device))
    model.to(device)

    model.eval()
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for batch in test_data_loader:
            # start = time.time()

            inputs = {key: val.to(device) for key, val in batch.items()}
            targets = batch["target_tag"].to(device)

            outputs, _ = model(**inputs)
            preds = outputs.argmax(2)  # Prendre l'indice de la classe la plus probable

            # stop=time.time()
            # print(stop-start)
            

            # Déplier les séquences et filtrer les labels à ignorer (-100)
            active_preds = preds.view(-1)
            active_targets = targets.view(-1)

            valid_idx = active_targets != -100
            all_preds.extend(active_preds[valid_idx].cpu().numpy())
            all_targets.extend(active_targets[valid_idx].cpu().numpy())
            

    # Calculer les métriques détaillées pour toutes les classes
    target_names = list(enc_tag.keys())
    detailed_report = classification_report(
        all_targets, all_preds, target_names=target_names, output_dict=True
    )

    # Mapper les étiquettes vers les catégories générales
    general_targets = map_to_general_labels(all_targets)
    general_preds = map_to_general_labels(all_preds)

    # Calculer les métriques pour les catégories générales
    general_target_names = ["O", "PER", "LOC", "ORG", "MISC"]
    general_report = classification_report(
        general_targets, general_preds, target_names=general_target_names, output_dict=True
    )

    # Exporter les rapports en JSON
    with open(config.RESULT_DETAIL_PATH, "w") as f:
        json.dump(detailed_report, f, indent=4)

    with open(config.RESULT_GENERAL_PATH, "w") as f:
        json.dump(general_report, f, indent=4)

    print("Rapports exportés : detailed_report.json et general_report.json")
