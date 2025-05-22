from pydantic import BaseModel
from abc import ABC, abstractmethod
from enum import Enum
from properties.domain.repositories import PropertyRepository
from typing import Union

class PropertyState(Enum):
    PRE_VENTA = "pre_venta"
    EN_VENTA = "en_venta"
    VENDIDO = "vendido"


class PropertyRequest(BaseModel):
    anio_construcion: Union[int, None] 
    ciudad: Union[str, None]
    estado: PropertyState

class PropertyResponse(BaseModel):
    direccion: str
    ciudad: str
    estado: str
    precio_venta: int
    descripcion: str


class CreateProperty:

    def __init__(self, property_repository: PropertyRepository):
        self._property_repository = property_repository

    
    def find_properties(self, property_filters: PropertyRequest):
        all_properties = self._property_repository.get_all(property_filters)
        return all_properties




        


        
