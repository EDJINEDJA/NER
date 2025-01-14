import pandas as pd
import numpy as np

import joblib
import torch
import json

from sklearn import preprocessing
from sklearn import model_selection

from transformers import get_linear_schedule_with_warmup

import config
import dataset
import trainer
from model import EntityModel
import ast

def split_data(data_path):

    #lire des données
    data = pd.read_csv(data_path, encoding="UTF-8")

    # Conversion des valeurs de la colonne 'sentence' en entiers (si nécessaire)
    data['sentences'] = pd.to_numeric(data['sentences'], errors='coerce')

    # Filtrage des lignes en fonction des valeurs de la colonne 'sentence'
    part1 = data[(data['sentences'] >= 0) & (data['sentences'] <= 300)]
    part2 = data[(data['sentences'] >= 301) & (data['sentences'] <= 1000)]

    # Enregistrement des nouvelles parties dans le dossier de sortie
    part1_file = config.TEST_FILE
    part2_file = config.TRAINING_FILE

    part1.to_csv(part1_file, index=False)
    part2.to_csv(part2_file, index=False)


def process_data(data_path):
    df = pd.read_csv(data_path, encoding="UTF-8")

    enc_tag = config.CLASSES

    df["nertags"] = df["nertags"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
    df["chunktags"] = df["chunktags"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
    df["nertags"] = df["nertags"].apply(
    lambda item: [enc_tag.get(str(tag), 0) for tag in item]
    )
    sentences = df.groupby("sentences")["chunktags"].apply(list).values

    tag = df.groupby("sentences")["nertags"].apply(list).values

    return sentences, tag, enc_tag


if __name__ == "__main__":

    split_data(config.ARTIFACT_DATA_PATH )
    
    sentences, tag, enc_tag = process_data(config.TRAINING_FILE)

    num_tag =config.NUM_TAG

    (
        train_sentences,
        test_sentences,
        train_tag,
        test_tag
    ) = model_selection.train_test_split(sentences, tag, random_state=42, test_size=0.25)

    train_dataset = dataset.CustomDataset(
        texts=train_sentences, tags=train_tag
    )


    train_data_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=config.TRAIN_BATCH_SIZE, num_workers=4
    )

    valid_dataset = dataset.CustomDataset(
        texts=test_sentences, tags=test_tag
    )

    valid_data_loader = torch.utils.data.DataLoader(
        valid_dataset, batch_size=config.VALID_BATCH_SIZE, num_workers=1
    )

    device = torch.device("cuda")
    model = EntityModel(num_tag=num_tag)
    model.to(device)

    param_optimizer = list(model.named_parameters())
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    optimizer_parameters = [
        {
            "params": [
                p for n, p in param_optimizer if not any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.001,
        },
        {
            "params": [
                p for n, p in param_optimizer if any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.0,
        },
    ]

    num_train_steps = int(len(train_sentences) / config.TRAIN_BATCH_SIZE * config.EPOCHS)
    optimizer =  torch.optim.AdamW(optimizer_parameters, lr=3e-4)
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=num_train_steps
    )

    best_loss = np.inf

    state_train = []
    state_test = []
    epochs = []
    states_results = {}

    for epoch in range(config.EPOCHS):
        train_loss = trainer.train_fn(train_data_loader, model, optimizer, device, scheduler)
        test_loss = trainer.eval_fn(valid_data_loader, model, device)

        state_train.append(train_loss)
        state_test.append(test_loss)
        epochs.append(epoch)

        print(f"Train Loss = {train_loss} Valid Loss = {test_loss}")
        if test_loss < best_loss:
            torch.save(model.state_dict(), config.MODEL_PATH)
            best_loss = test_loss

    states_results["state_train"] = state_train
    states_results["state_test"] = state_test
    states_results["epochs"] = epochs

    with open(config.MODEL_REPORT_PATH, "w") as f:
        json.dump(states_results, f, indent=4)