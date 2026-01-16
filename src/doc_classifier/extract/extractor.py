from typing import Literal
from pathlib import Path
from typing import Optional
import pandas as pd

import fitz  # PyMuPDF
from docx import Document # python-docx

BBDD_FULL_PATH = "C:/Users/mamen/Desktop/Project/Assigment 3 - Klynt AG/data/messy_folder/"

FileType =  Literal[".pdf", ".pptx", ".xlsx", ".docx"]

class Extractor():

    def __init__(self, file_name):

        self.file_name = file_name
        self.file_type: Optional[FileType]

        self.select_extractor_type()


    def select_extractor_type(self):

        self.file_type = (Path(self.file_name).suffix).lower()

    def extract_pdf(self):
        text = ""
        doc = fitz.open(BBDD_FULL_PATH + self.file_name)
        for i, page in enumerate(doc):
            text += page.get_text("text")
        return text
    
    def extract_docx(self):
        text = ""
        doc = Document(BBDD_FULL_PATH + self.file_name)
        text = "\n".join(p.text for p in doc.paragraphs)
        return text 
    
    def extract_xlsx(self):
        sheets = pd.read_excel(BBDD_FULL_PATH + self.file_name, sheet_name=None)
        parts = []
        for name, df in sheets.items():
            parts.append(f"=== {name} ===")
            parts.append(df.astype(str).fillna("").to_string(index=False))
        return "\n".join(parts)


    def extract_content(self):

        if self.file_type == ".pdf":
            return self.extract_pdf()
        
        elif self.file_type == ".docx":
            return self.extract_docx()
        
        elif self.file_type == ".xlsx":
            return self.extract_xlsx()
         
        elif self.file_type == ".png":
            return f'Need OCR'
        
        else:
            return "Type not supported"
        
    
    def normalizing_text(self, text: str):
        text = text.lower()

        # set de tokens (palabras)
        tokens_list = text.split()

        # texto normalizado
        normalized_text = " ".join(tokens_list)

        return tokens_list, normalized_text

    