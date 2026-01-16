# main.py -> python -m src.doc_classifier.main

from ingest import Ingestor
from report import generate_json
from extract.extractor import Extractor
from classifier.classifier import Classifier

if __name__ == "__main__":

    path_messy_folder = "C:/Users/mamen/Desktop/Project/Assigment 3 - Klynt AG/data/messy_folder"
    
    ingestor = Ingestor(path_messy_folder)
    list_files_name = ingestor.get_files()

    list_reports = []
    
    for name in list_files_name[:2]:

        e = Extractor(name)
        file_content = e.extract_content()
        token_list , normalized_text = e.normalizing_text(file_content)
       

        c = Classifier()
        #report = c.get_heuristic_name_score(file_name = name)
        report_2 = c.get_heuristic_from_content(token_list=token_list, normalized_text=normalized_text, file_name=name)

        

        #list_reports.append(report)
        # ahora llamamos al 'classifier' para que corra las Heuristicas y genere un report para el archivo
    
    #classification_report = generate_json(list_reports)

    #print(classification_report)
