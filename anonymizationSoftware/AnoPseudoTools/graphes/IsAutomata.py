"""
ce code représente l'algorithme utilisé pour reconnaître les élements qui 
appartiennent à un langage. 
"""
from AnoPseudoTools.graphes.AddPatterns import AddPartterns
import re 
from typing import List

class IsAutomata():
    def __init__(self) -> None:
        parser= AddPartterns()
        self.grapheLoc=parser.addPatternsGraphLoc()
        self.graphePer=parser.addPatternsGraphPer()
        self.grapheOrg=parser.addPatternsGraphOrg()
        self.FinitsState={"FinitsStateLoc":["S04","S12","S22","S35","S42","S50","T04","U05",
        "P03", "U10", "P12","G06","E05"],
        "FinitsStatePer":["A02","B04","A12","B14","B22","B30","B41","B51","B63","B71","B82","B91","B105","C05","C15","C23","C30","C32","C41","D02","F04",
        "G10","G04"],
         "FinitsStateOrg":["H02","H20","H30","H14","J02","O03","O14","O24","K03","K11"]}

    @staticmethod
    def str2list(word : str) -> List[str]: 
        return word.split(" ")

    def isAutomataLoc(self, pattern : str )-> bool:
        try:
            NextState='S00' 
            for entity in self.str2list(pattern):
                q0=NextState
                NextState=self.grapheLoc.successors(NextState)
                for item in NextState:
                    if self.grapheLoc.arc_weight((q0,item))==entity:
                        NextState=item
                
            if NextState in self.FinitsState["FinitsStateLoc"]:
                return True
            return False
        except TypeError:
            return False
    
    def isAutomataPer(self, pattern : str )-> bool:
        try:
            NextState='S100' 
            for entity in self.str2list(pattern):
                q0=NextState
                NextState=self.graphePer.successors(NextState)
                for item in NextState:
                    if self.graphePer.arc_weight((q0,item))==entity:
                        NextState=item
                
            if NextState in self.FinitsState["FinitsStatePer"]:
                return True
            return False
        except TypeError:
            return False

    def isAutomataOrg(self, pattern : str )-> bool:
        try:
            NextState='S200' 
            for entity in self.str2list(pattern):
                q0=NextState
                NextState=self.grapheOrg.successors(NextState)
                for item in NextState:
                    if self.grapheOrg.arc_weight((q0,item))==entity:
                        NextState=item
                
            if NextState in self.FinitsState["FinitsStateOrg"]:
                return True
            return False
        except TypeError:
            return False



       
        
       
