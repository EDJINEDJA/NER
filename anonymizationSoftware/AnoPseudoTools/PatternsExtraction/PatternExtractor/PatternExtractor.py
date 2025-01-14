from typing import List
from configparser import ConfigParser
import pandas as pd 
import re
import os 



from AnoPseudoTools.PatternsExtraction.PatternExtractor.Models.Models import Models

config=ConfigParser()
config.read(f"""{os.path.join(os.path.dirname(__file__),"..","Config","config.ini")}""")

class PatternExtractor():
    
    def __init__(self, pickleState :  bool) -> None:
        models=Models()
        self.tagger=models.load_trained_models(pickle=pickleState)
    
    def patternExtractor(self, P : str):
        """_summary_

        Args:
            [P (_type_=str): _description_= text in string format
            eg: <PER> Nicolas </PER> is a student]
        """
        
        "We want to delete all the tags inside the text P to be able to use the POS template properly"
        parserTagsRe=re.compile("<PER>|</PER>|<LOC>|</LOC>|<MISC>|</MISC>|<ORG>|</ORG>")
        P1=parserTagsRe.sub("",P)
    
        "POS entyties extraction"
        entitiesPos=self.tagger(P1)

        "get list of words"
        parserWordsRe=re.compile(r"\w+|\W+") 
        words=parserWordsRe.findall(P)

        "Replace all words per their POS category"
        for index_i,item_i in enumerate(words):
            for  item_j in entitiesPos:
                if item_i==item_j['word']:
                    words[index_i]=item_j['entity_group'] + ' '

        "delete all punctuations within pattern"         
        words=[''.join(letter for letter in word if letter not in """!#$%&()"*+,-.:;=?@[\]^_`{|}~""") for word in words]
        patternWithPunctuation="".join(words)
        
        "Delete all punctuations"
        pattern=re.sub(r">",'> ',patternWithPunctuation)
        parserCommaRe=re.compile("j'|c'|m'|l'|n'|t'|s'|d'|z'|q'")
        pattern=parserCommaRe.sub("CLS ",pattern)
        parserVerbRe=re.compile("'ai|'est|'es")
        pattern=parserVerbRe.sub("V ",pattern)

        formulatedPattern=""    
        for item in entitiesPos: 
            formulatedPattern=formulatedPattern + item['entity_group'] + " "
            
        formulatedPattern=formulatedPattern[:-1] #delete blanc
        return pattern,formulatedPattern,entitiesPos

    def patternExtractorShiftReduce (self, P : str):

        pattern,formulatedPattern ,entitiesPos= self.patternExtractor(P)
        
        #Shift-reduce operation (we will reduce the number of entities a bit by replacing the entity by the most generalized entity 
        # eg: Nom = NC/NPP and Adj= ADJ/ADJWH
        chunkGVRe=re.compile("\sV\sVPP\sVINF\s|\sV\sVPP\s|\sV\sVIMP\s|\sV\sVPP\s|\sV\sVPR\s|\sVINF\s|\sV\sVS\s|\sV\s|\sVPP\s|\sVINF\s|\sVPP\s|\sVPR\s|\sVS|VINF\s")
        pattern=chunkGVRe.sub(" GV ", pattern)
        formulatedPattern=chunkGVRe.sub(" GV ", formulatedPattern)

        chunkGVRe=re.compile("\sGV\sGV\s|\sGV\sGV\sGV\s|\sGV\sGV\sGV\sGV\s")
        pattern=chunkGVRe.sub(" GV ", pattern)
        formulatedPattern=chunkGVRe.sub(" GV ", formulatedPattern)

        chunkGNRe=re.compile(" NPP NPP| NP CC NPP| NPP NPP NPP| NPP NPP NPP NPP| NPP| NPP NPP NPP NPP NPP| NPP NPP|NPP | NPP ")
        pattern=chunkGNRe.sub(" GN ", pattern)
        formulatedPattern=chunkGVRe.sub(" GN ", formulatedPattern)

        chunkGVRe=re.compile("\sGN\sGN\s|\sGN\sGN\sGN\s|\sGN\sGN\sGN\sGN\s")
        pattern=chunkGVRe.sub(" GV ", pattern)
        formulatedPattern=chunkGVRe.sub(" GV ", formulatedPattern)

       
        pattern=pattern.strip() # delete the blanc space around the entyuties concatenated
        formulatedPattern=formulatedPattern.strip()
       
        return pattern,formulatedPattern,entitiesPos
    
    
    def patternsExtractor(self, listP : List[str], fileName : str):
        """_summary_
        Args:
            listP (List[str]): list of sentences
        """
        
        libraryOutput={"Sentences":[],"Patterns":[],"formulatedPatterns":[]}
        
        for item in listP:
            pattern,formulatedPattern,entitiesPos = self.patternExtractorShiftReduce(item)
            libraryOutput["Sentences"].append(item)
            libraryOutput["Patterns"].append(pattern)
            libraryOutput["formulatedPatterns"].append(formulatedPattern)
            
        Data=pd.DataFrame(libraryOutput)
        
        
        return Data.to_excel (r"{}/{}.xlsx".format(os.path.join(os.path.dirname(__file__),"..","ExcelFiles"),fileName), index = False, header=True)

    def lastMatchBelong2EndBoundary(self,entitySentence : List[str], startCompt : int ):
        # eg : ['DET', 'NC', 'P', 'NC'] start with CLS return the last item if item belong to the last item of CLS
        try:

            if len(entitySentence[startCompt+1:])==0 or len(entitySentence[startCompt+1:])==1:
                return []

            elif entitySentence[startCompt] == "CLS":
                allMatchPossible = [item for item in entitySentence[startCompt+1 : ] if item in config.get("CLS","end")]
                if len(allMatchPossible)==0:
                    pass
                else:
                    return allMatchPossible[-1]

            elif entitySentence[startCompt]=="DET":
                allMatchPossible = [item for item in entitySentence[startCompt+1 : ] if item in config.get("DET","end")]
                if len(allMatchPossible)==0:
                    pass
                else:
                    return allMatchPossible[-1]

            elif entitySentence[startCompt]=="DETWH":
                allMatchPossible = [item for item in entitySentence[startCompt+1 : ] if item in config.get("DETWH","end")]
                if len(allMatchPossible)==0:
                    pass
                else:
                    return allMatchPossible[-1]
            
            elif entitySentence[startCompt]=="P":
                allMatchPossible = [item for item in entitySentence[startCompt+1 : ] if item in config.get("P","end")]
                if len(allMatchPossible)==0:
                    pass
                else:
                    return allMatchPossible[-1]

            elif entitySentence[startCompt]=="VIMP":
                allMatchPossible = [item for item in entitySentence[startCompt+1 : ] if item in config.get("VIMP","end")]
                if len(allMatchPossible)==0:
                    pass
                else:
                    return allMatchPossible[-1]

            elif entitySentence[startCompt]=="NC":
                allMatchPossible = [item for item in entitySentence[startCompt+1 : ] if item in config.get("NC","end")]
                if len(allMatchPossible)==0:
                    pass
                else:
                    return allMatchPossible[-1]

            elif entitySentence[startCompt]=="ADV":
                allMatchPossible = [item for item in entitySentence[startCompt+1 : ] if item in config.get("ADV","end")]
                if len(allMatchPossible)==0:
                    pass
                else:
                    return allMatchPossible[-1]

            elif entitySentence[startCompt]=="PRO":
                allMatchPossible = [item for item in entitySentence[startCompt+1 : ] if item in config.get("PRO","end")]
                if len(allMatchPossible)==0:
                    pass
                else:
                    return allMatchPossible[-1]

            elif entitySentence[startCompt]=="V":
                allMatchPossible = [item for item in entitySentence[startCompt+1 : ] if item in config.get("V","end")]
                if len(allMatchPossible)==0:
                    pass
                else:
                    return allMatchPossible[-1]
        except IndexError:
            pass
        
    def matchPattern(self, P : str):
        try:
            #Pattern extraction 
            pattern,formulatedPattern ,entitiesPos = self.patternExtractorShiftReduce(P)
           
            entitySentence=formulatedPattern.split(" ")
            startCompt=[]
            endCompt=[]
            #Match pattern
            for index,item in enumerate(entitySentence):
                if item in config.get("boundary","begining"):
                    startCompt.append(index)
                   
                    if len(self.lastMatchBelong2EndBoundary(entitySentence , index))==0: # return [],[],[] if the are not values that correspond end value of the start entity
                        endCompt.append(index)
                        
                    else:
                
                        endItem=[index1 for index1,item1 in enumerate(entitySentence) if item1==self.lastMatchBelong2EndBoundary(entitySentence , index)]
                        if len(endItem)==0:
                            endCompt.append(index)
                        else:
                            endCompt.append(endItem[-1])
                    
                else:
                    pass
            
            listPatternsMatched=[entitySentence[i:j+1] for i,j in zip(startCompt,endCompt)]
            listPatternsConcatenated=[" ".join(item) for item in listPatternsMatched]

            listPatternsConcatenatedEndWithGN=[item + " GN" for item in listPatternsConcatenated]
            listPatternsConcatenatedStartWithGN=["GN " + item for item in listPatternsConcatenated]
            
            return listPatternsConcatenatedEndWithGN, listPatternsConcatenatedStartWithGN, entitiesPos

        except TypeError:
            
            return [],[],[]
        

                    

        
        
        
        
        
        
        
        
    
    