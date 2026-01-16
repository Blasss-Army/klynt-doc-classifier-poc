
import re
from report import DocumentRecord
import yaml
from typing import List
import random
import math

TAXONOMY_PATH = "C:/Users/mamen/Desktop/Project/Assigment 3 - Klynt AG/configs/taxonomy.yaml"
RULES_PATH = "C:/Users/mamen/Desktop/Project/Assigment 3 - Klynt AG/configs/rules.yaml"

class Classifier():

    def __init__(self , threshold:int = 0.75):

        self.threshold = threshold
    

    def get_taxonomy_document_type(self, taxonomy_dic:dict):
        text = ""
        for k, v in taxonomy_dic.items():
            for k_2, v_2 in v.items():
                    text += k_2 + "|"
        return text[:-1]
    
    def get_heuristic_name_score(self, match_score: float = 0.6, file_name: str = None) -> DocumentRecord:

        with open(TAXONOMY_PATH , "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)   # <- devuelve dict/list (estructura Python)
                data= data['taxonomy']

        types = self.get_taxonomy_document_type(data)
        x = re.search(rf"({types})", file_name , re.IGNORECASE) 
        
        if x:
            
            document_type = str(x.group(0))

            # document_type = invoice 
            # suggested_folder = Financial
            # confidence = 0.6
            # confidence_report = Medium
            # flags = [....] 
            
            for k,v in data.items():
                for k_2 , v_2 in v.items():
                    if k_2.lower() == document_type:
                        folder = k
                        d_type = k_2


            return DocumentRecord(file_path= 'messy_folder/' + file_name, document_type= d_type, suggested_folder= folder, confidence= match_score)


    def generate_bias(self):

        return round(random.uniform(0.0, 0.2), 2)
    

    def softmax_normalization(self, scores: dict):
         
        mx = max(scores.values())
        exps = {k: math.exp(v - mx) for k, v in scores.items()}  # estable numéricamente
        Z = sum(exps.values())
        return {k: round(e / Z, 2) for k, e in exps.items()}


    def get_heuristic_from_content(self, w1:float = 0.32, w2:float = 0.14, w3:float = 0.26, token_list: List[str] = [] , normalized_text: str = "" , file_name: str = None) -> DocumentRecord:

        # - bias (random -> 0.0 a 0.2)
        # - strong_phrases
        # - keywords
        # - negative_keywords

        # Score = bias + num_strong_phrases_matched(0.32) + num_keywords_matched(0.14) - num_negative_keywords_matched(0.26)
        #         --------------------------------------------------------------------------------------------------
        # Softmax (normalizacion) 0 - 1

        set_token = set(token_list)

        with open(RULES_PATH , "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)   # <- devuelve dict/list (estructura Python)
                data= data['rules']  
        
        scores = {}  
        
        for k, v in data.items():

            strong = 0
            keyword = 0
            negative = 0

            strong_phrases = v['strong_phrases']
            keywords = v['keywords']
            negative_keywords = v['negative_keywords']

            for i in strong_phrases:
                 if i in normalized_text:
                      strong += 1
            
            for j in keywords:
                 if j in set_token:
                      keyword += 1

            for z in strong_phrases:
                 if z in negative_keywords:
                      negative += 1

            b = self.generate_bias()
     
            score = b + (strong*w1) + (keyword*w2) - (negative*w3)

            scores[k] = score
       
        normalized_scores = self.softmax_normalization(scores)



    def run(self, file_content):
         
        if len(file_content)==0:
              # Need OCR porque es un escaner / Imagen
              pass

        
