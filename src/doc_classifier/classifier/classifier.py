
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
                        d_type = k_2

            return {d_type: 0.6}
        
        return {}
            #return DocumentRecord(file_path= 'messy_folder/' + file_name, document_type= d_type, suggested_folder= folder, confidence= match_score)


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
       
        return self.softmax_normalization(scores)



    def aggregator(self, h1_scores_dic:dict = {}, h2_scores_dic:dict = {}, w1: int = 0.3, w2:int = 0.75, k_top:int = 3):
         
        # Score = score_h1(0.3) + score_h2(0.65)

        if len(list(h1_scores_dic)) == 0:
             return -1
        
        h1_type =list(h1_scores_dic)[0]

        for k, v in h2_scores_dic.items():
            if h1_type == k:

                new_score = round((h1_scores_dic[h1_type]*w1) + (v*w2),2)
                h2_scores_dic[k] = new_score
                
        list_top_k_3 = sorted(h2_scores_dic.values(), reverse=True)[:3]


        sort = {}

        for k,v in h2_scores_dic.items():

            if v in list_top_k_3:
                sort[k] = v
        

        return sort


    def generate_flags(self, top_k_dic:dict[str,float]) -> List[str]:
         
        values = sorted(top_k_dic.values(), reverse=True)

        if (values[0] - values[1]) > 0.2:
            return ['HIGH CONFIDENCE']
        
        elif ((values[0] - values[1]) <= 0.1) and (values[0]> 0.15):
            return ['AMBIGUOUS','MULTI_LABEL']
        
        elif ((values[0] - values[1]) <= 0.1) and (values[0]<= 0.15):
            return ['AMBIGUOUS']
        
        else:
             return ['CLASSIFIED']



    def get_top_document_type(self,  top_k_dic:dict[str,float])->str:
          
        return max(top_k_dic, key=top_k_dic.get)
    
    def get_top_document_folder(self,  document_type:str)->str:
         
        with open(TAXONOMY_PATH , "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)   # <- devuelve dict/list (estructura Python)
                data= data['taxonomy']
        
        for k, v in data.items():
             if document_type in v:
                  return k



        
