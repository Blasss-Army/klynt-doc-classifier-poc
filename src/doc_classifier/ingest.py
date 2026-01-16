# ingest.py

import os 

class Ingestor ():

    '''Recorres todos los archivos del folder y guardas todos los nombres en una lista (eso es lo q se devuelve)'''
    
    def __init__(self, path_folder = "C:/Users/mamen/Desktop/Project/Assigment 3 - Klynt AG/data/messy_folder/messy_folder"):
        self.path_folder = path_folder


    def get_files(self):
        return [name for dirpath, _, filenames in os.walk(self.path_folder) for name in filenames ]
         