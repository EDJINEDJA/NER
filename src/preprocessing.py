import os
import numpy as np
from pathlib import Path
from glob import glob
from striprtf.striprtf import rtf_to_text
import re
WORKDIR= os.getcwd()

def preprocessing():
    """ The aims of this function is to transform a rtf file into a txt file
    """
    
    #reads all file path using glob
    
    files = glob(pathname=os.path.abspath(os.path.join(WORKDIR, "data/data/transcriptions/*.rtf")))

    #extract all text inside using striprtf
    for file in files:

        try:
            with open(file, mode='r', encoding='utf-8') as f:
                    contenu_rtf = f.read()
        except UnicodeDecodeError:
            print("Erreur de décodage avec UTF-8, tentative avec Windows-1252...")
            with open(file, mode='r', encoding='windows-1252') as f:

                contenu_rtf = f.read()
                print("tentative réussit ...")
        
        texts = rtf_to_text(contenu_rtf)

        #Extract the file name
        filename = os.path.basename(file)

        #Now make a path to new file name, in order to save the file (txt)
        with open(os.path.abspath(os.path.join(WORKDIR, f'data/artifact/{filename}.txt')) , 'w', encoding='utf-8') as f:

            f.write(texts)

if __name__=='__main__':
    preprocessing()
    


