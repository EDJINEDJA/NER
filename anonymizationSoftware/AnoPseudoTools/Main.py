''' If folders architecture uncomment this'''
import json
import os
from pathlib import Path

from AnoPseudoTools.TokenEntity import TokenEntity
from AnoPseudoTools.Models import Models
from AnoPseudoTools.Anotator_transformers import Anotator_transformers


class Main:
    def __init__(self,loadTrainedModels=False,pickleState=False):
        self.anotatorTransformers=Anotator_transformers(loadTrainedModels,pickleState)
        

    def pseudonymization(self, file_path:str):
        text= self.anotatorTransformers.pseudonymization(file_path)
        return text

    def anonymization(self, file_path:str):
        output = self.anotatorTransformers.anonymisation(file_path)
        return output

    def displacy(self, file_path:str):
        output = self.anotatorTransformers.display(file_path)
        return output
    
    def get_score(self, results_path: str, syntetic_path:str, model: str):
        self.anotatorTransformers.getscore(results_path, syntetic_path, model)
        
        
    def save_parse_as_json(self, file_path:str,folder:str):
        # dump the archive as json file
        print("Saving archive parse ▪️▪️▪️/▪️▪️▪️")
        parser= self.anotatorTransformers.pseudonymization(file_path)
        file_name=Path(file_path).stem
        with open(os.path.join(folder,f"archive2{file_name}.json"), 'w', encoding="utf-8") as f:
             json.dump(parser, f)