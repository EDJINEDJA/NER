import re
import os
import glob
import time
import ollama
import random
import pickle
import instructor
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv
from typing import (List,Dict, Tuple)


from saveresults import save_dict_to_folder
WORKDIR= os.getcwd()


def disrupter(Text: str, NAME: List[str], SURNAME: List[str], LOC: List[str], ORG: List[str], MISC: List[str], MISC1: List[str]) -> Tuple[str, dict]:
    """
    Remplace les tokens dans le texte par des valeurs aléatoires issues des listes correspondantes
    et retourne le texte modifié ainsi qu'un dictionnaire des valeurs remplacées.

    Args:
        Text (str): Texte contenant des tokens à remplacer.
        NAME, SURNAME, LOC, ORG, MISC (List[str]): Listes de valeurs pour chaque type d'entité.

    Returns:
        Tuple[str, dict]: Texte modifié et dictionnaire des remplacements effectués.
    """
    # Associer les types d'entités aux listes correspondantes
    entity_lists = {
        "@@NAME": NAME,
        "@@SURNAME": SURNAME,
        "@@LOC": LOC,
        "@@ORG": ORG,
        "@@MISC": MISC,
        "@@MISC1": MISC1
    }

    # Initialisation des résultats
    epsilonJson = {}
    modified_text = Text

    for entity_tag, values in entity_lists.items():
        # Trouver toutes les correspondances pour le tag actuel
        matches = list(re.finditer(re.escape(entity_tag), modified_text))
        count = len(matches)

        # Si aucune correspondance, passer à l'entité suivante
        if count == 0:
            # Si c'est @@MISC et qu'il n'y a pas de correspondances, assigner MISC à une liste vide
            if entity_tag == "@@MISC":
                epsilonJson["MISC"] = []
            if entity_tag == "@@MISC1":
                epsilonJson["MISC1"] = []
            continue

        # Générer des remplacements aléatoires
        replacements = random.choices(values, k=count)
        epsilonJson[entity_tag.strip("@@")] = replacements

        # Reconstruction du texte avec les remplacements
        new_text = []
        last_end = 0

        for match, replacement in zip(matches, replacements):
            start, end = match.span()
            # Ajouter le texte avant le match, puis le remplacement
            new_text.append(modified_text[last_end:start])
            new_text.append(replacement)
            last_end = end

        # Ajouter la fin du texte
        new_text.append(modified_text[last_end:])
        modified_text = ''.join(new_text)

    return modified_text, epsilonJson



def processtext(TEXT: str) -> Tuple[str, dict]:

    with open( os.path.abspath(os.path.join(WORKDIR, "data/Objects/NAME")), 'rb') as f1:
        NAME = pickle.load(f1)
    f1.close()

    with open(os.path.abspath(os.path.join(WORKDIR, "data/Objects/SURNAME")), 'rb') as f1:
        SURNAME = pickle.load(f1)
    f1.close()

    with open(os.path.abspath(os.path.join(WORKDIR, "data/Objects/LOC")), 'rb') as f1:
        LOC = pickle.load(f1)
    f1.close()

    with open(os.path.abspath(os.path.join(WORKDIR, "data/Objects/ORG")), 'rb') as f1:
        ORG = pickle.load(f1)
    f1.close()

    with open(os.path.abspath(os.path.join(WORKDIR, "data/Objects/MISC")), 'rb') as f1:
        MISC = pickle.load(f1)
    f1.close()

    with open(os.path.abspath(os.path.join(WORKDIR, "data/Objects/MISC1")), 'rb') as f1:
        MISC1 = pickle.load(f1)
    f1.close()


    disruptedText, epsilonJson = disrupter(TEXT, NAME, SURNAME, LOC, ORG, MISC, MISC1)

    return disruptedText , epsilonJson

def synteticCorpusGenerator(size : int, path_raw_text: Path, pathsyntetic: Path, filename: str):

    files = glob.glob(pathname=path_raw_text)

    synteticTexts = {}

    for idx in range(size):

        file = random.choices(files)

        path = file[0]

        with open(path, mode="r") as f:
            Text =  f.readlines()
        f.close()

        Text= "".join(Text)

        disruptedText , epsilonJson = processtext(Text)

        synteticTexts[idx] = {"text": disruptedText , "true_values" : epsilonJson}

    save_dict_to_folder(synteticTexts, pathsyntetic, filename)

     

if __name__=='__main__':
    synteticCorpusGenerator(size = 1000, path_raw_text= os.path.abspath(os.path.join(WORKDIR, "data/data/ManAno/ANO/*.txt")), pathsyntetic=os.path.abspath(os.path.join(WORKDIR, "data/synteticcorpus/")), filename="corpus")