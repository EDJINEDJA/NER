import os
import transformers


WORKDIR = os.getcwd()

RAW_DATA_PATH = os.path.abspath(os.path.join(WORKDIR, "camembertft/input/raw/corpus.json"))

ARTIFACT_DATA_PATH = os.path.abspath(os.path.join(WORKDIR, "camembertft/input/artifact/corpus.csv"))

TRAINING_FILE = os.path.join(WORKDIR, "camembertft/input/artifact/train.csv")

TEST_FILE = os.path.abspath(os.path.join(WORKDIR, "camembertft/input/artifact/test.csv"))

TEST_BATCH_SIZE= 1

MAX_LEN = 256

TRAIN_BATCH_SIZE = 32

VALID_BATCH_SIZE = 8

EPOCHS = 20

BACKBONE = "camembert-base"

LOSS_IGNORE_INDEX = -100

CLASSES = {'O': 0, 
               'B-PER': 1, 'I-PER': 2,
                'B-LOC': 3, 'I-LOC': 4,
                'B-ORG': 5, 'I-ORG': 6,
                'B-MISC': 7, 'I-MISC': 8
            }

NUM_TAG = 9

propagate_label_to_word_pieces = True

TOKENIZER = transformers.AutoTokenizer.from_pretrained(BACKBONE)

MODEL_PATH=os.path.join(WORKDIR, "camembertft/input/Camembertft/Camembertft.pth'")

MODEL_REPORT_PATH = os.path.join(WORKDIR, "camembertft/input/Camembertft/model_report.json")

RESULT_DETAIL_PATH=os.path.join(WORKDIR, "camembertft/input/Camembertft/detailed_report.json")

RESULT_GENERAL_PATH=os.path.join(WORKDIR, "camembertft/input/Camembertft/general_report.json")