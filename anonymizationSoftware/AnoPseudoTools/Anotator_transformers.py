''' If folders architecture uncomment this'''
import re
import json
import os
import pandas as pd
import time
import glob

from AnoPseudoTools.TokenEntity import TokenEntity
from AnoPseudoTools.Models import Models
from AnoPseudoTools.Loadfile import Loadfile
from typing import Dict
from dataclasses import dataclass

from AnoPseudoTools.saveresults import save_dict_to_folder
from AnoPseudoTools.evaluator import evaluate

class Anotator_transformers():
      """
      Anotator_ do pseudonymisation , anonymisation , and display using html file
      """
      def __init__(self,loadTrainedModels=False,pickleState=False):
            models = Models()
            self.loadfile= Loadfile()

            if loadTrainedModels:
              ner_dates, tagger  = models.load_trained_models(pickle=pickleState)
            #ner_dates, tagger  = models.load_pickled_models()

            self.tokenEntity = TokenEntity(ner_dates, tagger)
   
            self.regex_pattern_number='un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|dixsept|dixhuit\
                              |dixneuf|vingt|vingtetun|vingtdeux|vingttrois|vingtquatre|vingtcinq|vingtsix|vingtsept|vingthuit|vingtneuf|trente|trenteetun|trentedeux|trentetrois\
                              |trentequatre|trentecinq|trentesix|trentesept|trentehuit|trenteneuf|quarante|quaranteetun|quarantedeux|quarantetrois|quarantequatre|quarantecinq\
                              |quarantesix|quarantesept|quarantehuit|quaranteneuf|cinquante|cinquanteetun|cinquantedeux|cinquantetrois|cinquantequatre|cinquantecinq|cinquantesix\
                              |cinquantesept|cinquantehuit|cinquanteneuf|soixante|soixanteetun|soixantedeux|soixantetrois|soixantequatre|soixantecinq|soixantesix|soixantesept\
                              |soixantehuit|soixanteneuf|soixantedix|septante|soixanteetonze|septanteetun|soixantedouze|septantedeux|soixantetreize|septantetrois|soixantequatorze\
                              |septantequatre|soixantequinze|septantecinq|soixanteseize|septantesix|soixantedixsept|septantesept|soixantedixhuit|septantehuit|soixantedixneuf\
                              |septanteneuf|quatrevingts|huitante|quatrevingtun|huitanteetun|quatrevingtdeux|huitantedeux|quatrevingttrois|huitantetrois|quatrevingtquatre\
                              |huitantequatre|quatrevingtcinq|huitantecinq|quatrevingtsix|huitantesix|quatrevingtsept|huitantesept|quatrevingthuit|huitantehuit|quatrevingtneuf\
                              |huitanteneuf|quatrevingtdix|nonante|quatrevingtonze|nonanteetun|quatrevingtdouze|nonantedeux|quatrevingttreize|nonantetrois|quatrevingtquatorze\
                              |nonantequatre|quatrevingtquinze|nonantecinq|quatrevingtseize|nonantesix|quatrevingtdixsept|nonantesept|quatrevingtdixhuit|nonantehuit|quatrevingtdixneuf|nonanteneuf|cent '

            self.regex_pattern_email='[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@apple.com|[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@outlook.com\
                              |[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@hotmail.com|[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@mail.com\
                              |[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@yahoo.com|[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@gmail.com\
                              |[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@apple.fr|[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@outlook.fr\
                              |[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@hotmail.fr|[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@mail.fr\
                              |[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@yahoo.fr|[AZERTYUIOPMLKJHGFDSQWXCVBN1234567890.,!*$:;?azertyuiopmlkjhgfdsqwxcvbnà=)ç_è-'"é&"')]*@gmail.fr'
                              
            self.regex_pattern =  self.regex_pattern_number+"|"+self.regex_pattern_email   
               
      @staticmethod
      def myReplace(text,Word,subWord):
          pattern=re.compile('\.')
          text=pattern.sub(' .',text)
          list_words=text.split()
          for index , word in enumerate(list_words):
              if word==Word:
                  list_words[index]=subWord
          return " ".join(list_words)

      @staticmethod
      def numberNoiseMakers(archive_number,text):
          for word in archive_number:
              if word =="deux":
                text=text.replace(word,"trois")
              elif word=="trois":
                text=text.replace(word,"quatre")
              elif word=="quatre":
                text=text.replace(word,"cinq")
              elif word=="cinq":
                text=text.replace(word,"six")
              elif word=="six":
                text=text.replace(word,"sept")
              elif word=="sept":
                text=text.replace(word,"huit")
              elif word=="huit":
                text=text.replace(word,"neuf")
              elif word=="neuf":
                text=text.replace(word,"dix")
              elif word=="dix":
                text=text.replace(word,"onze")
              elif word=="onze":
                text=text.replace(word,"douze")
              elif word=="douze":
                text=text.replace(word,"treize")
              elif word=="treize":
                text=text.replace(word,"quartoze")
              elif word=="quartoze":
                text=text.replace(word,"quinze")
              elif word=="quinze":
                text=text.replace(word,"seize")
              else:
                pass
          return text
        
          
      #pseudonymization
      def entity_changer_pseudonymization(self,text,archive,token_entity,unique_token_set,entity_type,nameofreplacement):
          number=1
          for unique_token in unique_token_set:
              #pippeline to replace all entity name 
              if token_entity[f'{unique_token}']==f'{entity_type}':
                archive["archive_word"][f"{nameofreplacement}{number}"] = f"{unique_token}"
                text=self.myReplace(text,f'{unique_token}',f"""{nameofreplacement}{number}""")
                number =number+1
              else :
                  pass
          return archive,text
          
      def regex_changer_pseudonymization(self,text):
          #replace all E-Mail per E-Mail
          pattern_re_email = self.regex_pattern_email
          repl = f"E-Mail"
          text=re.sub(pattern_re_email ,repl,text)
          return text

      #anonymization
      def entity_changer_anonymisation(self,text,token_entity,unique_token_set,entity_type):
          for unique_token in unique_token_set:
              #pippeline to replace all entity name 
              if token_entity[f'{unique_token}']==f'{entity_type}':
                text=self.myReplace(text,f'{unique_token}',f'{unique_token}')
              else :
                  pass
          return text
          
      def regex_changer_anonymisation(self,text):
          #replace all E-Mail per E-Mail
          pattern_re_email = self.regex_pattern_email
          repl = ""
          text=re.sub(pattern_re_email ,repl,text)
          return text

          
      def pseudonymization(self,file_path)->str:
          """re commnly call regular expression for turn all number in xx
          json dump the archive file
          """

          archive={"Description":"Archive of all words changed during the process",
                "archive_word": {},"archive_number":{"postion_start":[],"postion_end":[],"words":[]}}
          
          
          #init
          parser=self.loadfile.read_file(file_path)

          #token entity
          start = time.time() 
          token_entity=self.tokenEntity.processing(parser.sentence_txt)
          print(token_entity)
          stop = time.time()
          print(f"process time:{stop-start}")

          #compute the unique token 
          token=list(token_entity.keys())
          unique_token_set=set(token)
          #replace and store in archive part
          iter_words=re.finditer(self.regex_pattern,parser.sentence_txt)

          for iter in iter_words:
              archive["archive_number"]["postion_start"].append(iter.start())
              archive["archive_number"]["postion_end"].append(iter.end())
              archive["archive_number"]["words"].append(iter.group())
          
          text= self.numberNoiseMakers(archive["archive_number"]["words"],parser.sentence_txt)
  
          archive,text=self.entity_changer_pseudonymization(parser.sentence_txt,archive,token_entity,unique_token_set,"PER","Nom")
          archive,text=self.entity_changer_pseudonymization(text,archive,token_entity,unique_token_set,'LOC',"Ville")
          archive,text=self.entity_changer_pseudonymization(text,archive,token_entity,unique_token_set,'ORG',"Organisation")
          archive,text=self.entity_changer_pseudonymization(text,archive,token_entity,unique_token_set,'MISC',"Divers")
          
          #replace  all E-Mail per E-Mail
          text=self.regex_changer_pseudonymization(text)
          
          #Insert the rest of the pseudonymization in the database
          person=[(k,val) for (k,val)  in archive["archive_word"].items() if re.match("Nom\d+",k)!=None]
          Person=""
          for (k,val) in person:
            Person=Person+f"{k}:{val}"+","
            
          localization= [(k,val) for (k,val)  in archive["archive_word"].items() if re.match("Ville\d+",k)!=None]
          Localization=""
          for (k,val) in localization:
            Localization=Localization+f"{k}:{val}"+","
            
          organization=[(k,val) for (k,val)  in archive["archive_word"].items() if re.match("Organisation\d+",k)!=None]
          Organization=""
          for (k,val) in organization:
            Organization=Organization+f"{k}:{val}"+","
            
          miscellaneous=[(k,val) for (k,val)  in archive["archive_word"].items() if re.match("Divers\d+",k)!=None]
          Miscellaneous=""
          for (k,val) in miscellaneous:
            Miscellaneous=Miscellaneous+f"{k}:{val}"+","
          
          return text

      def display(self,file_path):
          """
          display share the html file for good visualisation
          the process is the same
          """
          token_entity={}
          # library of all number in text
          number_in_text={"archive_number":{"words":[]}}
          
          #init
          parser=self.loadfile.read_file(file_path)
          
          #archive all number
          iter_words=re.finditer(self.regex_pattern,parser.sentence_txt)

          for iter in iter_words:
            number_in_text["archive_number"]["words"].append(iter.group())
            
          name_number,town_number,org_number,misc_number=1,1,1,1
          
          #token entity
          token_entity=self.tokenEntity.processing(parser.sentence_txt)

          token=list(token_entity.keys())
          # unique_token_set=set(token)
          unique_token_set=token

          # Add noise to numbers
          text= self.numberNoiseMakers(number_in_text["archive_number"]["words"],parser.sentence_txt)
          
          #replace all E-Mail per E-Mail
          pattern_re_email = self.regex_pattern_email
          style__=f"""<mark class="entity" style="background: #f38714; padding: 0.2em 0.3em; margin: 0 0.1em; line-height: 1; border-radius: 0.35em;"> E-Mail
                                <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem"> E-Mail </span> 
                    </mark> 
                """
          text=re.sub(pattern_re_email,style__,text)

          for unique_token in unique_token_set:
            #pippeline to replace all name per the name between 1 until the total of unique name
            if token_entity[f'{unique_token}']=='PER':
              style___=f""" <mark class="entity" style="background: #3ca9e2; padding: 0.2em 0.3em; margin: 0 0.10em; line-height: 1; border-radius: 0.35em;">
                                  Nom{name_number}
                                  <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem"> PER </span>
                          </mark> """
              text=text.replace(f'{unique_token}', style___)
              name_number=name_number+1
              #pippeline to replace all town per the name between 1 until the total of unique town
            elif token_entity[f'{unique_token}']=='LOC':
              style____=f""" <mark class="entity" style="background: #0C0; padding: 0.2em 0.3em; margin: 0 0.1em; line-height: 1; border-radius: 0.35em;">
                              Ville{town_number}
                              <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem"> LOC </span>
                            </mark> """
              text=text.replace(f'{unique_token}',style____ )
              town_number=town_number+1
            #pippeline to replace all organisation per the name between 1 until the total of unique organisation
            elif token_entity[f'{unique_token}']=='ORG':
              style_____=f""" <mark class="entity" style="background: #8a8b8e; padding: 0.2em 0.3em; margin: 0 0.1em; line-height: 1; border-radius: 0.35em;"> 
                                    Organisation{org_number}
                                    <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem"> ORG </span> 
                              </mark>
                        """
              text=text.replace(f'{unique_token}',style_____)
              org_number=org_number+1
            elif token_entity[f'{unique_token}']=='MISC':
              style_____=f""" <mark class="entity" style="background: #8a8b8e; padding: 0.2em 0.3em; margin: 0 0.1em; line-height: 1; border-radius: 0.35em;"> 
                                    Divers{misc_number}
                                    <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem"> MISC </span> 
                            </mark>
                        """
              text=text.replace(f'{unique_token}',style_____)
              misc_number=misc_number+1
            pass
          html = (
                  "<div style='max-width:100%; max-height:360px; overflow:auto'>"
                                + text
                    + "</div>"
                )
          return html

      def anonymisation(self,file_path)-> str:
          '''
          delete all word matched.
          the process is the same
          '''
          
          token_entity={}

          # library of all number in text
          number_in_text={"archive_number":{"words":[]}}

          #init
          parser=self.loadfile.read_file(file_path)
          
          #archive all number
          iter_words=re.finditer(self.regex_pattern,parser.sentence_txt)

          for iter in iter_words:
            number_in_text["archive_number"]["words"].append(iter.group())
         
          #token entity
          token_entity=self.tokenEntity.processing(parser.sentence_txt)

          token=list(token_entity.keys())
          unique_token_set=set(token)
         
          text=self.entity_changer_anonymisation(parser.sentence_txt,token_entity,unique_token_set,"PER")
          text=self.entity_changer_anonymisation(text,token_entity,unique_token_set,'LOC')
          text=self.entity_changer_anonymisation(text,token_entity,unique_token_set,'ORG')
          text=self.entity_changer_anonymisation(text,token_entity,unique_token_set,'MISC')
          
          # Add noise to numbers
          text= self.numberNoiseMakers(number_in_text["archive_number"]["words"],text)
    
          #replace all E-Mail per E-Mail
          text=self.regex_changer_anonymisation(text)
          
          return text
      
      def getscore(self,results_path: str, syntetic_path:str, model: str):
        """re commnly call regular expression for turn all number in xx
        json dump the archive file
        """

        files = glob.glob(os.path.abspath(os.path.join(results_path,"*.json")))

        with open(syntetic_path, mode="r", encoding='utf-8') as f:
            data = json.load(f)
        f.close

        if files==[]:

          true_values = data["0"]["true_values"]
          disruptedText = data["0"]["text"] 
          filename = "run_0"

          
          entities =self.tokenEntity.processing(disruptedText)

          response_json = self.group_entities( entities)

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


            entities = self.tokenEntity.processing(disruptedText)

            response_json = self.group_entities(entities)

            score = evaluate(response_json, true_values)

            dicts_to_save = {
                "model": model,
                "score": score,
            }

            save_dict_to_folder(dicts_to_save, results_path, filename)

      def group_entities(self, entities):
        grouped = {'PER': [], 'LOC': [], 'ORG': [], 'MISC': []}

        for word, label in entities.items():
         
          if label=='DATE':
            grouped['MISC'].append(word)
          else:
            grouped[label].append(word)
             

        return grouped
