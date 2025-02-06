
import pandas as pd
import json
from pathlib import Path
import config
import re

import nltk
from nltk.corpus import stopwords
import string

class Preprocessing():
    def __init__(self, config: config):

        self.raw_data_path = config.RAW_DATA_PATH

        nltk.download('stopwords')

        # Liste des stopwords en français
        self.stop_words = set(stopwords.words('french'))

        # Ajouter la ponctuation à la liste des stopwords
        punctuation = set(string.punctuation)
        self.stop_words.update(punctuation)

        # Ajouter des phrases ou mots spécifiques comme "fre"
        self.stop_words.update(["fre", "Scribe3", "Document", ''])


    def process(self):

        with open(self.raw_data_path, mode='r') as f:
            data = json.load(f)
        f.close()

        ponctuation_sauf_point = string.punctuation.replace('.', '')

        sentences = []

        chunktags = []

        nertags = []


        for id, item in data.items():


            texts = item.get("text")

            pattern0="\[\d+\:\d+\:\d+\.\d+\]|\[\d+]|\--|Scribe3|Date: \d+\-\d+\-\d+|Document: \d+\-\d+.wma|Duration: \d+.\d+s|Language: fre \(auto\)|Type: cts"
            pattern1="\\n"
            pattern2="           "
            pattern3='-'
            pattern4='\s+'

            try:
                text = re.sub(pattern0,'', texts)
                text = re.sub(pattern1,'   ',text)
                text = re.sub(pattern2,'.',text)
                text = re.sub(pattern3 ,'',text)
                text = re.sub(pattern4, ' ', text)
                text = re.sub(r'\n+', '\n', text)
                text = text.replace("\r", "\n").replace("\t", " ")
            except Exception as e:
                pass

            # Supprimer ces ponctuations
            text = text.translate(str.maketrans('', '', ponctuation_sauf_point))
            
            lignes = text.split('\n')
            lignes_non_vides = [ligne for ligne in lignes if ligne.strip() != ' ']
            text ='\n'.join(lignes_non_vides)


            tags = item.get("true_values")
            for item in ["NAME","SURNAME","LOC","ORG","MISC"]:
                if  item not in tags.keys():
                    tags[item]=[]


            LNAMES = [item.split() for item in tags["NAME"]]
            LSURNAMES = [item.split() for item in tags["SURNAME"]]
            LLOCS = [item.split() for item in tags["LOC"]]
            LORGS = [item.split() for item in tags["ORG"]]
            LMISCS = [item.split() for item in tags["MISC"]]

            entities = LNAMES + LSURNAMES + LLOCS + LORGS + LMISCS

            entitieswithoutlist = [item for sublist in entities for item in sublist]

            tokens  = text.split(".")

            for text in tokens:

                text=text.strip()

                ner_tag= []

                token = text.split(" ")

                #token = [mot for mot in token if mot not in self.stop_words or mot == '.']

                token = [item for item in token if item != []]

                if len(token)==0 or token ==['']:

                    pass

                else:

                    for item in token:

                        if item in entitieswithoutlist:

                            for lnames in LNAMES:

                                if item in lnames:

                                    idx = lnames.index(item)

                                    if idx==0:

                                        ner_tag.append('B-PER')
                                    else:
                                        ner_tag.append('I-PER')
                                    break

                            for lsurnames in LSURNAMES:

                                if item in lsurnames:

                                    idx = lsurnames.index(item)

                                    if idx==0:

                                        ner_tag.append('B-PER')
                                    else:
                                        ner_tag.append('I-PER')
                                    break

                            for llocs in LLOCS:

                                if item in llocs:

                                    idx = llocs.index(item)

                                    if idx==0:

                                        ner_tag.append('B-LOC')
                                    else:
                                        ner_tag.append('I-LOC')
                                    break
                            
                            for lorgs in LORGS:

                                if item in lorgs:

                                    idx = lorgs.index(item)

                                    if idx==0:

                                        ner_tag.append('B-ORG')
                                    else:
                                        ner_tag.append('I-ORG')
                                    break

                            for lmiscs in LMISCS:

                                if item in lmiscs:

                                    idx = lmiscs.index(item)

                                    if idx==0:

                                        ner_tag.append('B-MISC')
                                    else:
                                        ner_tag.append('I-MISC')
                                    break
                        else:
                            ner_tag.append('O')
                        
                if len(token)==len(ner_tag):
                    chunktags.append(token)
                    nertags.append(ner_tag)
                    sentences.append(id)

        dataf = pd.DataFrame(data={'sentences': sentences, 'chunktags': chunktags, 'nertags': nertags})
        dataf.to_csv(config.ARTIFACT_DATA_PATH)

            
                


if __name__=='__main__':

    parser = Preprocessing(config)
    parser.process()