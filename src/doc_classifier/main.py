# main.py -> python -m src.doc_classifier.main

from ingest import Ingestor
from report import generate_json
if __name__ == "__main__":

    path_messy_folder = "C:/Users/mamen/Desktop/Project/Assigment 3 - Klynt AG/data/messy_folder/messy_folder"
    
    ingestor = Ingestor(path_messy_folder)
    list_files_name = ingestor.get_files()

    classification_report = generate_json(list_files_name)

    print(classification_report)
