import pandas as pd
from pathlib import Path
import pickle
import os
import re
from typing import List
from ep import data

WORKDIR = os.getcwd()

NAME = []

SURNAME = []

ORG = [ "Lidl"]

LOC = []

MISC = [

]

MISC1 = [
    "zéro deux trente-sept vingt-et-un cinquante-trois zéro huit",
    "zéro six quatre-vingt-dix zéro neuf vingt-cinq soixante-huit",
    "zéro trois quarante-deux cinquante-huit trente-sept onze",
    "zéro cinq soixante-onze dix-huit quatre-vingts quarante-six",
    "zéro un cinquante-quatre quatre-vingt-trois trente-huit zéro sept",
    "zéro sept vingt-huit soixante-quatorze cinquante-neuf vingt-trois",
    "zéro quatre soixante-deux quatre-vingt-six dix-sept trente-et-un",
    "zéro six trente-quatre quarante-huit cinquante-deux zéro neuf",
    "zéro un quarante-cinq quatre-vingt-onze zéro huit trente-trois",
    "zéro deux vingt-trois cinquante-neuf soixante-dix-huit douze",
    "zéro six soixante-trois quatre-vingt-sept trente-deux onze",
    "zéro cinq quarante-huit soixante-dix-neuf vingt-et-un zéro trois",
]


def loadNames(path: Path, NAME : List[str], outputdir: Path):
    
  data =   pd.read_csv(path, sep=",")

  names = data["patronyme"].apply(lambda x : str(x).lower().capitalize())

  NAME = NAME + list(names)

  with open(os.path.join(outputdir, "NAME"), 'wb') as f1:
    pickle.dump(NAME, f1)

def loadSurNames(path: Path, SURNAME : List[str], outputdir: Path):
    
  data =   pd.read_csv(path, sep=",")

  Surname= data["prenom"].apply(lambda x : str(x).lower().capitalize())

  SURNAME = SURNAME + list(Surname)

  with open(os.path.join(outputdir, "SURNAME"), 'wb') as f1:
    pickle.dump(SURNAME, f1)


def move_parenthesis_to_front(text):
    
  match = re.search(r'\((.*?)\)', text)  # Trouver le contenu entre parenthèses
  if match:
      content = match.group(1)  # Extraire le contenu des parenthèses
      text = f"{content} {text.replace(f'({content})', '').strip()}"  # Placer le contenu devant
  return text

def loadLoc(data : str, LOC : List[str], outputdir: Path):

  lines = data.strip().split("\n")
  formatted_list = [move_parenthesis_to_front(line.strip()) for line in lines if line.strip()]


  LOC = LOC + formatted_list 

  with open(os.path.join(outputdir, "LOC"), 'wb') as f1:
    pickle.dump(LOC, f1)


def loadOrg(path: Path, ORG : List[str], outputdir: Path):

  data =   pd.read_csv(path, sep=",")

  Org = data["NOM_DISPOSITIF"].apply(lambda x : str(x).lower().capitalize())

  ORG = ORG + list(Org)

  with open(os.path.join(outputdir, "ORG"), 'wb') as f1:
    pickle.dump(ORG, f1)

def loadMisc(MISC : List[str], outputdir: Path):

  MISC = MISC

  with open(os.path.join(outputdir, "MISC"), 'wb') as f1:
    pickle.dump(MISC, f1)

def loadMisc1(MISC1 : List[str], outputdir: Path):

  MISC1 = MISC1

  with open(os.path.join(outputdir, "MISC1"), 'wb') as f1:
    pickle.dump(MISC1, f1)


if __name__=="__main__":
  loadNames(Path(os.path.abspath(os.path.join(WORKDIR,"data/data/per/patronymes.csv"))), NAME, Path(os.path.abspath(os.path.join(WORKDIR,"data/Objects/"))))
  loadSurNames(Path(os.path.abspath(os.path.join(WORKDIR,"data/data/per/prenom.csv"))), SURNAME, Path(os.path.abspath(os.path.join(WORKDIR,"data/Objects/"))))
  loadOrg(Path(os.path.abspath(os.path.join(WORKDIR,"data/data/org/geocoded.csv"))), ORG, Path(os.path.abspath(os.path.join(WORKDIR,"data/Objects/"))))
  loadLoc(data, LOC, Path(os.path.abspath(os.path.join(WORKDIR,"data/Objects/"))))
  loadMisc(MISC,  Path(os.path.abspath(os.path.join(WORKDIR,"data/Objects/"))))
  loadMisc1(MISC1,  Path(os.path.abspath(os.path.join(WORKDIR,"data/Objects/"))))
  



