"""
    Santiago Bobadilla
    Juan José Beltrán
    MODELOS
"""

# Librerias
from pydantic import BaseModel
from typing import List

# Abstracto medico + Enfermedad
class CompDataModel (BaseModel):
    medical_abstracts: str
    problems_described: int 

# Lista de Abstractos medicos + su enfermedad
class ListDataModel (BaseModel):
    data: List[CompDataModel]

def all_name():
    return ['medical_abstracts', 'problems_described']
