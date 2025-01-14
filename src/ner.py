
import re
import os
import glob
import time
import ollama
import random
import pickle
from pydantic import BaseModel
import instructor
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv
from typing import (List,Dict, Tuple)
import json

from entities import  ResponseModel
from saveresults import save_dict_to_folder
from evaluator import evaluate


WORKDIR= os.getcwd()

load_dotenv()



def generate_prompt(text: str) -> str:
    prompt = """  
    Your task is to identify and extract sensitive information such us:
        - Proper Names (PER) 
        - Geographic informations (LOC)
        - Organizations (ORG)
        - Telephone numbers written in textual format that begin with 'zéro' or numbers such as: 'cent quarante-quatre, quinze, cent dix-sept' (MISC).

    Extract the entities for the following labels from the given text and provide the results in JSON format.
        - Entities must be extracted exactly as mentioned in the text.
        - Telephone numbers such as 'cent quarante-quatre', 'quinze' or 'cent dix-sept' must come from the text.
        - Return each entity under its label without creating new labels.
        - Provide a list of entities for each label, ensuring that if no entities are found for a label, an empty list is returned.
        - Accuracy and relevance in your responses are key.

    labels:
        - PER
        - LOC
        - ORG
        - MISC

    JSON format:
        {"PER":[],"LOC":[],"ORG":[],"MISC":[]}
    """
    return prompt


def groq_ner(text:str, model: str)-> Dict[str,List[str]]:

    prompt = generate_prompt(text)

    client = Groq(
        # This is the default and can be omitted
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    client = instructor.from_groq(client, mode=instructor.Mode.JSON)


    response = client.chat.completions.create(

        response_model=ResponseModel,

        messages=[
            {
                "role": "system",
                "content": "Your are a helpful anonymization assistant."
            },
            {
                "role": "user",
                "content": prompt,
            },

            {
                "role": "user",
                "content": text,
            }
        ],
        model=model,

        temperature=0,

    )

    # Dictionnaire des entités réelles (annotations)
    predictions  = {
        'PER': response.PER,
        'LOC': response.LOC,
        'ORG': response.ORG,
        'MISC': response.MISC
    }

    return predictions


def get_score(results_path: str, syntetic_path:str, model:str):

    files = glob.glob(os.path.abspath(os.path.join(results_path,"*.json")))

    with open(syntetic_path, mode="r", encoding='utf-8') as f:
        data = json.load(f)
    f.close

    if files==[]:

        true_values = data["0"]["true_values"]
        disruptedText = data["0"]["text"] 
        filename = "run_0"

        response_json = groq_ner(disruptedText,model)

        score = evaluate(response_json, true_values)

        dicts_to_save = {
            "model": model,
            "score": score,
        }

        save_dict_to_folder(dicts_to_save, results_path, filename)
    else:

        idxs = [int(item.split("_")[-1].split(".")[0]) for item in files]

        filename = "run_" + str(max(idxs)+1)

        true_values = data[f"{max(idxs)+1}"]["true_values"]
        disruptedText = data[f"{max(idxs)+1}"]["text"] 

        response_json = groq_ner(disruptedText,model)

        score = evaluate(response_json, true_values)

        dicts_to_save = {
            "model": model,
            "score": score,
        }

        save_dict_to_folder(dicts_to_save, results_path, filename)

def inference(syntetic_path:str, model:str):


    with open(syntetic_path, mode="r", encoding='utf-8') as f:
        data = json.load(f)
    f.close

    disruptedText = data["0"]["text"] 

    response_json = groq_ner(disruptedText,model)

    print(response_json)






if __name__=="__main__":

    model="llama3-70b-8192"

    results_path = os.path.abspath(os.path.join(WORKDIR, "data/results"))

    syntetic_path = os.path.abspath(os.path.join(WORKDIR, "data/synteticcorpus/corpus.json"))

    get_score(results_path, syntetic_path= syntetic_path, model=model)

    # start = time.time()
    # inference(syntetic_path, model)
    # stop = time.time()
    # print(f"process time:{stop-start}")
