''' If folders architecture uncomment this '''
import re
from AnoPseudoTools.Models import Models
from AnoPseudoTools.PatternsExtraction.PatternExtractor.PatternExtractor import PatternExtractor
from AnoPseudoTools.graphes.IsAutomata import IsAutomata

class TokenEntity():
    def __init__(self, ner_dates, tagger):
      self.models= Models()
      self.ParsserPE=PatternExtractor("False")
      self.IsA=IsAutomata()
      self.ner_dates, self.tagger  = ner_dates, tagger

    @staticmethod
    def splitText(text : str):

       return re.split(r' *[\.\?!][\'"\)\]]* *', text)
    
    @staticmethod
    def readDictFile():
        import json
        # Opening JSON file
        f = open('/home/laris/laris/NER/anonymizationSoftware/Models/dict.json')
        # returns JSON object as a dictionary
        data = json.load(f)

        return data

    def firstProcessing(self, text , pattern):
        # Uses a library to retrieve all sensitive entities in the text. (Library based approach)
        dict = self.readDictFile()
        chunkText = re.split(r"[\b\W\b]+", text)

        setWordLoc= set (dict["word_loc"])
        setWordper= set (dict["word_per"])
        setWordorg= set (dict["word_org"])

        for word in chunkText:

            if word in setWordLoc:
                pattern['word_loc'].append(word)
            elif word in setWordper:
                pattern['word_per'].append(word)
            elif word in setWordorg:
                pattern['word_org'].append(word)
            else:
                pass
       
        return pattern 

    def secondProcessing(self, text):
        #Get Entities  using JeanBaptiste CamemBert models (Data-driven based approach)
        entities = self.ner_dates(text)
        return entities

    def thirdProcessing(self, text , pattern ):

        #Makes the grammatical analysis and gives the grammatical syntax of the text (rules based approach)
        pos=self.tagger(text)

        bad_pos_for_panding_pos=[{'entity': '', 'score': 0.0742340236902237, 'word': ''},
         {'entity': '', 'score': 0.9995399713516235, 'word': ''},
         {'entity': '', 'score': 0.9999609589576721, 'word': ''},
         {'entity': '', 'score': 0.9999597072601318, 'word': ''},
         {'entity': '', 'score': 0.9999597072601318, 'word': ''},
         {'entity': '', 'score': 0.9999597072601318, 'word': ''}]

        pos.extend(bad_pos_for_panding_pos)
        
        odonym={'pont','route','Allée','anse','avenue','boulevard','carrefour','chaussée','chemin','cité','clos','côte','cour','cours','degré','descente','drève','escoussière',\
                'esplanade','gaffe','impasse','liaison','mail','montée','passage','place','placette','promenade','quai','résidence','rang','rampe','rond-point','rue','ruelle','sente','sentier',\
                'squade','traboule','traverse','venelle','villa','voie','berge','digue','escallier','giratoire','jardin','parvis','passerelle'}
        keywords = {'madame' , 'Madame' , 'monsieur' , 'Monsieur', 'professeur' , 'Professeur' , 'Prof' , 'Mr' , 'mr', 'Mdme' , 'mme' , 'Dr', 'docteur' , 'Docteur', 'dr',
        }
        
        #Uses a library to retrieve  all sensitive location entities in the text. 
        for id in range(len(pos)):
            if pos[id]['entity']=='NC' and pos[id]['word'].lower() in odonym:
               if pos[id+1]['entity']=='NC' or pos[id+1]['entity']=='NP' or pos[id+1]['entity']=='NPP':
                    pattern['word_loc'].append(pos[id]['word']+' '+pos[id+1]['word'])
               if pos[id+1]['entity']=='P' or pos[id+1]['entity']=='P+D':
                  if pos[id+2]['entity']=='P' or pos[id+2]['entity']=='P+D':
                     if pos[id+3]['entity']=='NC':
                        pattern['word_loc'].append(pos[id]['word']+' '+pos[id+1]['word']+' '+ pos[id+2]['word']+' '+ pos[id+3]['word'])
                     else:
                          pass
                  elif  pos[id+2]['entity']=='NC':
                        pattern['word_loc'].append(pos[id]['word']+' '+pos[id+1]['word']+' '+ pos[id+2]['word'])
                  else:
                      pass
               else:
                   pass
            else:
                pass

        #Uses a library to retrieve all sensitive person entities in the text.
        for id in range(len(pos)):
            if pos[id]['entity']=='NC' and pos[id]['word'].lower() in keywords:
               if pos[id+1]['entity']=='NC' or pos[id+1]['entity']=='NP' or pos[id+1]['entity']=='NPP':
                    pattern['word_per'].append(pos[id]['word']+' '+pos[id+1]['word'])
               if pos[id+1]['entity']=='P' or pos[id+1]['entity']=='P+D':
                  if pos[id+2]['entity']=='P' or pos[id+2]['entity']=='P+D':
                     if pos[id+3]['entity']=='NC':
                        pattern['word_per'].append(pos[id]['word']+' '+pos[id+1]['word']+' '+ pos[id+2]['word']+' '+ pos[id+3]['word'])
                     else:
                          pass
                  elif  pos[id+2]['entity']=='NC':
                        pattern['word_per'].append(pos[id]['word']+' '+pos[id+1]['word']+' '+ pos[id+2]['word'])
                  else:
                      pass
               else:
                   pass
            else:
                pass
        
        return pattern

    def fourthProcessing(self , text , token_entity):
        chunktext_=self.splitText(text)

        #Find entity like name of personne
        try:
            for itemText in chunktext_:
                # eg: ['CLS GV DET NC P GN', 'DET NC P GN', 'NC P GN', 'P GN'] ['GN CLS GV DET NC P', 'GN DET NC P', 'GN NC P', 'GN P']
                listPatternsEndWithGn,listPatternsStartWithGn,entities = self.ParsserPE.matchPattern(itemText)
            
                listBoolIsAutomataEndWithGn=[self.IsA.isAutomataPer(item) for item in  listPatternsEndWithGn]
                listBoolIsAutomataStartWithGn=[self.IsA.isAutomataPer(item) for item in  listPatternsStartWithGn]
                
                Truepatterns=[listPatternsEndWithGn[index].split(" ")[-2] for index , item in enumerate(listBoolIsAutomataEndWithGn) if item == True ]
                
                if len( Truepatterns)==0:
                    pass
                elif Truepatterns[0]=="NC" :
                    
                    keepIndex=[index for index , item in enumerate(entities) if item['entity_group'] == Truepatterns[0]]
                    for index in keepIndex:
                        if  index+1 > len(entities)-1 and entities[index+1]['entity_group'] in ["NP","NPP","NC"]:
                            token_entity[f"{entities[index+1]['word']}"]='PER'
                        elif entities[index+1]['entity_group'] in ["NP","NPP"]:
                            token_entity[f"{entities[index+1]['word']}"]='PER'
                        else:
                            pass
                else:
                    keepIndex=[index for index , item in enumerate(entities) if item['entity_group'] == Truepatterns[0]]

                    for index in keepIndex:
                        if  index+1 > len(entities) -1:
                            token_entity[f"{entities[index+1]['word']}"]='PER'
                           
                        else:
                            token_entity[f"{entities[index+1]['word']}"]='PER'
                            
                            
        except IndexError:
            pass
        
        #Find entity like name of locality

        try:
            for itemText in chunktext_:
                # eg: ['CLS GV DET NC P GN', 'DET NC P GN', 'NC P GN', 'P GN'] ['GN CLS GV DET NC P', 'GN DET NC P', 'GN NC P', 'GN P']
                listPatternsEndWithGn,listPatternsStartWithGn,entities = self.ParsserPE.matchPattern(itemText)
            
                listBoolIsAutomataEndWithGn=[self.IsA.isAutomataLoc(item) for item in  listPatternsEndWithGn]
                listBoolIsAutomataStartWithGn=[self.IsA.isAutomataLoc(item) for item in  listPatternsStartWithGn]
                
                Truepatterns=[listPatternsEndWithGn[index].split(" ")[-2] for index , item in enumerate(listBoolIsAutomataEndWithGn) if item == True ]
                
                if len( Truepatterns)==0:
                    pass
                elif Truepatterns[0]=="NC" :
                    keepIndex=[index for index , item in enumerate(entities) if item['entity_group'] == Truepatterns[0]]
                    for index in keepIndex:
                        if  index+1 > len(entities)-1 :
                            
                            token_entity[f"{entities[index+1]['word']}"]='LOC'
                        else:
                            token_entity[f"{entities[index+1]['word']}"]='LOC'
                else:
                    keepIndex=[index for index , item in enumerate(entities) if item['entity_group'] == Truepatterns[0]]

                    for index in keepIndex:
                        if  index+1 > len(entities) -1:
                            
                            token_entity[f"{entities[index+1]['word']}"]='LOC'
                           
                        else:
                            
                            token_entity[f"{entities[index+1]['word']}"]='LOC'
                            
                            
        except IndexError:
            pass


        try:
            for itemText in chunktext_:
                # eg: ['CLS GV DET NC P GN', 'DET NC P GN', 'NC P GN', 'P GN'] ['GN CLS GV DET NC P', 'GN DET NC P', 'GN NC P', 'GN P']
                listPatternsEndWithGn,listPatternsStartWithGn,entities = self.ParsserPE.matchPattern(itemText)
            
                listBoolIsAutomataEndWithGn=[self.IsA.isAutomataOrg(item) for item in  listPatternsEndWithGn]
                listBoolIsAutomataStartWithGn=[self.IsA.isAutomataOrg(item) for item in  listPatternsStartWithGn]
                
                Truepatterns=[listPatternsEndWithGn[index].split(" ")[-2] for index , item in enumerate(listBoolIsAutomataEndWithGn) if item == True ]
                
                if len( Truepatterns)==0:
                    pass
                elif Truepatterns[0]=="NC" :
                    keepIndex=[index for index , item in enumerate(entities) if item['entity_group'] == Truepatterns[0]]
                    for index in keepIndex:
                        if  index+1 > len(entities)-1 :
                            
                            token_entity[f"{entities[index+1]['word']}"]='ORG'
                        else:
                            token_entity[f"{entities[index+1]['word']}"]='ORG'
                else:
                    keepIndex=[index for index , item in enumerate(entities) if item['entity_group'] == Truepatterns[0]]

                    for index in keepIndex:
                        if  index+1 > len(entities) -1:
                            
                            token_entity[f"{entities[index+1]['word']}"]='ORG'
                           
                        else:
                            
                            token_entity[f"{entities[index+1]['word']}"]='ORG'                 
                            
        except IndexError:
            pass

        return token_entity
        


    def processing(self,text):
        #Part Dedicated To The Initialization 
        pattern={'word_loc':[],'word_misc':[],'word_per':[],'word_org':[]}
        token_entity={}

        #first processing
        pattern = self.firstProcessing(text , pattern)

        #second processing using ner model
        entities = self.secondProcessing(text)


        #Check Which Entities Have Been Found In The Sentence
        for entity in entities:
           
            token_entity[f"{entity['word'].lstrip('▁')}"]=entity["entity"].split('-')[-1]

        #Third processing using pos model and rules based methode . eg: Odonym + NC means NC = Location entity

        texts = text.split(".")
        
        
        for text in texts:

            pattern = self.thirdProcessing(text , pattern)
        
        #Uses a rule-based approach and calculations are performed using the DFA algorithm.
        token_entity = self.fourthProcessing(text , token_entity)
            
        #Add The New Token Entite Found Using POS
        for token in  pattern['word_loc']:
            token=re.sub(" ##","",token)
            token_entity[f"{token}"]='LOC'
        for token in  pattern['word_misc']:
            token=re.sub(" ##","",token)
            token_entity[f"{token}"]='MISC'
        for token in  pattern['word_per']:
            token=re.sub(" ##","",token)
            token_entity[f"{token}"]='PER'
        for token in  pattern['word_org']:
            token=re.sub(" ##","",token)
            token_entity[f"{token}"]='ORG'


        return  token_entity

