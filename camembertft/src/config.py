import os
from typing import Dict
from pathlib import Path
from transformers import AutoTokenizer
from dataclasses import dataclass, field

@dataclass
class Config():
    WORKDIR : Path = Path(os.getcwd())

    RAW_DATA_PATH : Path = Path(os.path.abspath(os.path.join(WORKDIR, "camembertft/input/raw/corpus.json")))

    ARTIFACT_DATA_PATH : Path = Path(os.path.abspath(os.path.join(WORKDIR, "camembertft/input/artifact/corpus.csv")))

    TRAINING_FILE : Path = Path(os.path.join(WORKDIR, "camembertft/input/artifact/train.csv"))

    TEST_FILE : Path = Path(os.path.abspath(os.path.join(WORKDIR, "camembertft/input/artifact/test.csv")))

    TEST_BATCH_SIZE : int = 1

    MAX_LEN : int = 120

    TRAIN_BATCH_SIZE : int = 32

    VALID_BATCH_SIZE : int = 8

    EPOCHS : int  = 10

    BACKBONE : str = "camembert-base"

    LOSS_IGNORE_INDEX : float = -100

    CLASSES : dict = field(default_factory=lambda:  {'O': 0, 
                'B-PER': 1, 'I-PER': 2,
                    'B-LOC': 3, 'I-LOC': 4,
                    'B-ORG': 5, 'I-ORG': 6,
                    'B-MISC': 7, 'I-MISC': 8
                })

    NUM_TAG : int = 9

    PROPAGATE_LABEL_TO_WORD_PIECES : bool = True

    TOKENIZER : AutoTokenizer = AutoTokenizer.from_pretrained(BACKBONE)

    MODEL_PATH : Path = Path(os.path.join(WORKDIR, "camembertft/input/Camembertft/Camembertft.pth"))

    MODEL_REPORT_PATH : Path = Path(os.path.join(WORKDIR, "camembertft/input/Camembertft/model_report.json"))

    RESULT_DETAIL_PATH : Path = Path(os.path.join(WORKDIR, "camembertft/input/Camembertft/detailed_report.json"))

    RESULT_GENERAL_PATH : Path = Path(os.path.join(WORKDIR, "camembertft/input/Camembertft/general_report.json"))