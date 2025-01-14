
from AnoPseudoTools.Main import Main
import os
import time

class PseudonymizationAnonymizationProcessing():
    def __init__(self,loadTrainedModels=False,pickleState=False):
        self.main = Main(loadTrainedModels,pickleState)
    

    def Pseudonymization(self,file):
        
        return self.main.pseudonymization(file)

    def Anonymization(self,file):

        return self.main.anonymization(file)
    
    def Displacy(self,file):

        return self.main.displacy(file)
    
    def GetScore(self,results_path,syntetic_path, model):
        
        self.main.get_score(results_path,syntetic_path, model)



if __name__=="__main__":

    WORKDIR= os.getcwd()

    model="neuro-symbolic"

    results_path = os.path.abspath(os.path.join(WORKDIR, "data/results"))

    syntetic_path = os.path.abspath(os.path.join(WORKDIR, "data/synteticcorpus/corpus.json"))

    parser=PseudonymizationAnonymizationProcessing(loadTrainedModels= True,pickleState=False)

    # parser.GetScore(results_path,syntetic_path, model)

    fileDir=os.path.join(os.path.dirname(__file__))
    fileName= os.path.join(os.getcwd(),"data/data/transcriptions/20210110-0000010.wma_fre_4.3-11185_rev0.rtf")
    # fileNameLink=fileDir + fileName
    fileNameLink= fileName
    parser.Pseudonymization(f"{fileNameLink}")

    job={0: "Default",
     1: "Pseudonymization",
     2: "Anonymization",
     3: "Html_Format"}

    Wich_Job=1
    NameJob=job[Wich_Job]

    if  NameJob=="Default":  
        
        print(parser.Pseudonymization(f"{fileNameLink}"))
        
    elif NameJob=="Pseudonymization":
        
        print(parser.Pseudonymization(f"{fileNameLink}"))
        
    elif NameJob== "Anonymization":
        
        print(parser.Anonymization(f"{fileNameLink}"))
       
    elif NameJob== "Html_Format":
        
        print(parser.Displacy(f"{fileNameLink}"))
        
    else:
        raise Exception("An error occurred")

