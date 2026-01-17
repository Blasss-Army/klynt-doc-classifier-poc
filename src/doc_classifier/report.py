# report.py

from typing import TypedDict, Literal, List, Optional, Dict, Any
from pathlib import Path
from typing import List, Literal
from pydantic import BaseModel, Field, computed_field
import json

class DocumentRecord(BaseModel):
    file_path: str
    document_type: str = "Unknown" 
    suggested_folder: str = "Needs_Review/"
    confidence: float = 0.0
    flags: List[str] = ["NOT_CLASSIFIED_YET"]

    @computed_field 
    @property
    def confidence_level(self) -> str:
        if self.confidence < 0.15:
            return "Low"
        elif self.confidence < 0.25:
            return "Medium"
        return "High"
 
def generate_report(file_name:str, document_type:str, suggested_folder:str, confidence:float, flags:List)-> DocumentRecord:

    if flags:
        return DocumentRecord(file_path= 'messy_folder/' + file_name, document_type= document_type, suggested_folder= suggested_folder, confidence= confidence, flags=flags)
    
    return DocumentRecord(file_path= 'messy_folder/' + file_name, document_type= document_type, suggested_folder= suggested_folder, confidence= confidence)

def generate_json(list_reports: List[DocumentRecord], base_dir: str = "messy_folder"):
    return json.dumps([report.model_dump() for report in list_reports if report is not None], indent=2, ensure_ascii=False)

