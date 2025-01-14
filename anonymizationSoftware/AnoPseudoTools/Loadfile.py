''' The content folder is a function that loads the file into the desired folder
and parses the file to return the text'''

import re
import os
from pathlib import Path
from AnoPseudoTools.PdfDocxDoc2Txt import PdfDocxDoc2Txt
from dataclasses import dataclass

@dataclass
class outLoadfile():
    sentence_txt : str
    file_name : str
    

class Loadfile():

  def __init__(self)-> None:
      self.PdfDocxDoc2Txt=PdfDocxDoc2Txt()
   

  def read_file(self, file)-> outLoadfile:
    """
    file : Give path of resume file
    """
    
    file = os.path.join(file)

    sentence_txt=""
    if file.endswith('pdf'):
        resume_lines, raw_text = self.PdfDocxDoc2Txt.convert_pdf2txt(file)
        sentence_txt=sentence_txt.join(resume_lines)
    elif file.endswith('txt'):
        with open(file, 'r',encoding="utf-8") as f:
            resume_lines = f.readlines()
            sentence_txt=sentence_txt.join(resume_lines)
    elif file.endswith('rtf'):
        sentence_txt=self.PdfDocxDoc2Txt.convert_rtf2text(file)
    elif file.endswith('docx'):
        resume_lines, raw_text=self.PdfDocxDoc2Txt.convert_docx2txt(file)
        sentence_txt=sentence_txt.join(resume_lines)
    elif file.endswith('doc'):
        resume_lines, raw_text=self.PdfDocxDoc2Txt.convert_doc2txt(file)
        sentence_txt=sentence_txt.join(resume_lines)

    else:
        resume_lines = ""
        sentence_txt=sentence_txt.join(resume_lines)
  
    #stem of the file_path 
    file_name=Path(file).stem
    return  outLoadfile(sentence_txt=sentence_txt,
                        file_name=file_name)

