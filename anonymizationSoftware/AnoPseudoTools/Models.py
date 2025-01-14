from transformers import AutoTokenizer,BertTokenizer, CamembertTokenizer,AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import pipeline
import pickle
import logging
import torch
import os
from AnoPseudoTools.cuda_detect import detect_cuda_device_number

WORKDIR = os.getcwd()

"""
Docstring: This script can be used as a file folder if you want to deploy.
Each field of code represents a file (.py).

Usage:
  - Folder: Annotator
    -> Models.py
    -> TokenEntity.py
    -> PdforDocs2Txt.py
    -> Loadfile.py
    -> Anotator_transformers.py
    -> Main.py
    -> APP (Pseudonymization app, Anonymization app, Html app)
    -> requirements.txt

Enable import if you want to deploy.
"""

__authors__ = ("LNIT INTERN 2022-2023", "LNIT")
__contact__ = ("LNIT")
__copyright__ = "MIT"
__date__ = "10/05/2022"
__version__ = "v8"


class Models:
    
    def __init__(self) -> None:
        self.device_number = detect_cuda_device_number()

        # Set up logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt='%m/%d/%Y %H:%M:%S',
            level=logging.INFO,
            handlers=[logging.StreamHandler()]
        )
        
        # Set device to GPU if available, else CPU
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def send2cuda(self, model):
        """
        Moves the model to the CUDA device if available, else keeps it on CPU.
        """
        if self._device.type == 'cuda':
            model.to(self._device)
        self.logger.info(f"Using model on device: {self._device}")
        return model

    def pickle_it(self, obj, file_name):
        """
        Saves an object (e.g., model) as a pickle file.
        """
        file_path = os.path.abspath(os.path.join(WORKDIR, f"anonymizationSoftware/Models/{file_name}.pickle"))
        with open(file_path, 'wb') as f:
            pickle.dump(obj, f)

    def unpickle_it(self, file_name):
        """
        Loads a pickled object from file.
        """
        file_path = os.path.abspath(os.path.join(WORKDIR, f"anonymizationSoftware/Models/{file_name}.pickle"))
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    def load_trained_models(self, pickle=False):
        """
        Loads pre-trained models for NER (Named Entity Recognition) and POS tagging.
        Optionally pickle the models.
        """
        try:
            # Load NER model (dates)
            # Load model directly
            tokenizer_ner = CamembertTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
            model_ner = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")
            self.ner_dates = pipeline('ner', model=model_ner, tokenizer=tokenizer_ner)

            # Load POS tagging model
            tokenizer_pos = CamembertTokenizer.from_pretrained("gilf/french-camembert-postag-model")
            model_pos = AutoModelForTokenClassification.from_pretrained("gilf/french-camembert-postag-model")
            self.ner_pos = pipeline('ner', model=model_pos, tokenizer=tokenizer_pos)

            if pickle:
                self.pickle_models()

            return self.ner_dates, self.ner_pos

        except Exception as e:
            self.logger.error("Error loading trained models: %s", str(e))
            raise

    def pickle_models(self):
        """
        Pickles the loaded models for later use.
        """
        self.pickle_it(self.ner_dates, "ner_dates")
        self.pickle_it(self.ner_pos, "pos_tagger_fast")

    def load_pickled_models(self):
        """
        Loads previously pickled models and moves them to the appropriate device.
        """
        try:
            ner_dates = self.unpickle_it('ner_dates')
            ner_dates = self.send2cuda(ner_dates)

            tagger = self.unpickle_it("pos_tagger_fast")
            tagger = self.send2cuda(tagger)

            return ner_dates, tagger
        
        except Exception as e:
            self.logger.error("Error loading pickled models: %s", str(e))
            raise
