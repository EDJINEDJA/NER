
''' If folders architecture uncomment this'''
import glob
import time 
import random 
from AnoPseudoTools.Main import Main
import os

class BatchPseudonymizationAnonymizationProcessing():
    def __init__(self,loadTrainedModels=False,pickleState=False):
        self.main = Main(loadTrainedModels,pickleState)
    
    def uniquekey(self):
        lower_case="abcdefghijklmnopqrstuvwxyz"
        upper_case="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        number="123456789"
        Use_for=lower_case+upper_case+number
        lenght_for_unique_key=8
        self.key="".join(random(Use_for,lenght_for_unique_key))
        return self.key

    def renderedPseudonymization(self,file):

        return self.main.pseudonymization(file)

    def renderedAnonymization(self,file):

        return self.main.anonymization(file)
     
    def BatchPseudonymizationAnonymizationProcessing_(self,rtfdocdocxpdf_folders):
        files_path=glob.glob(rtfdocdocxpdf_folders+"/*.*")
        curr_time = time.localtime()
        curr_clock = time.strftime("%a %b %d %Y %H:%M", curr_time)
        num=0

        #verified wheter the folder exist else creat new folder 
        if not os.path.isdir(os.path.join(rtfdocdocxpdf_folders)+"/data "+f"{curr_clock}"):
           os.makedirs(os.path.join(rtfdocdocxpdf_folders)+"/data "+f"{curr_clock}")
           new_folder=os.path.join(rtfdocdocxpdf_folders)+"/data "+f"{curr_clock}"
        else :
             key=self.uniquekey()
             os.makedirs(os.path.join(rtfdocdocxpdf_folders)+"/data "+f"{curr_clock} "+key)
             new_folder=os.path.join(rtfdocdocxpdf_folders)+"/data "+f"{curr_clock} "+ key

        #builded txt_pseudonymized_folder/ txt_pseudonymized_folder contain the pseudonymization file 
        if not os.path.isdir(new_folder+"/txt_pseudonymized_folder"):
            os.makedirs(new_folder+"/txt_pseudonymized_folder")

        #builded txt_pseudonymized_folder/ txt_pseudonymized_folder contain the pseudonymization file 
        if not os.path.isdir(new_folder+"/txt_anonymized_folder"):
            os.makedirs(new_folder+"/txt_anonymized_folder")
            
        #builded archive folder/ archivecontain the pseudonymization/anonymization archive 
        if not os.path.isdir(new_folder+"/archive"):
            os.makedirs(new_folder+"/archive")

        #Job   
        for file_path in files_path:
            text=self.renderedPseudonymization(file_path)
            text_anonymized=self.renderedAnonymization(file_path)
            self.main.save_parse_as_json(file_path,new_folder+"/archive")

            #Write pseudonymized text
            with open(f'{new_folder+"/txt_pseudonymized_folder"}'+f'/text{num}.txt','w',encoding="utf8") as f:
                f.write(text)
                
            #Write anonymized text
            with open(f'{new_folder+"/txt_anonymized_folder"}'+f'/text{num}.txt','w',encoding="utf8") as f:
                f.write(text_anonymized)
            num=num+1

            #remove the file after done the job / enable this if you want to deploye 
            os.remove(file_path)


# Change file_folder in order to setup right text folder 
parser=BatchPseudonymizationAnonymizationProcessing(loadTrainedModels=False,pickleState=False)
file_folder="./data"
parser.BatchPseudonymizationAnonymizationProcessing_(file_folder)