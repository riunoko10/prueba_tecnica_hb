import pytest
import httpx
from src.properties.domain.schemas import PropertyRequest, PropertyState
from src.properties.domain.repositories import PropertyRepository
from src.properties.application.value_objects import CreateProperty


inmuebles = [
    {
        "id": 1,
        "direccion": "Calle 123",
        "ciudad": "Madrid",
        "estado": "pre_venta",
        "precio_venta": 250000,
        "descripcion": "Piso moderno",
        "año_construccion": "2020"
    },
    {
        "id": 2,
        "direccion": "Avenida Principal 456",
        "ciudad": "Barcelona",
        "estado": "en_venta",
        "precio_venta": 180000,
        "descripcion": "Apartamento céntrico",
        "año_construccion": 2019
    },
        {
        "id": 3,
        "direccion": "Avenida Principal 456",
        "ciudad": "Barcelona",
        "estado": "en_venta",
        "precio_venta": 180000,
        "descripcion": "Apartamento céntrico",
        "año_construccion": 2021
    },
]


class FakePropertyRepository(PropertyRepository):

    def __init__(self):
        self._properties = inmuebles
    
    def get_all_filters(self, params):

        estado = params.estado if params and hasattr(params, "estado") else None
        resultado = [p for p in self._properties if p["estado"] == estado.value]

        if params.anio_construcion:
            resultado = [p for p in self._properties if p["año_construccion"] == estado.value]
        
        if hasattr(params, "ciudad"):
            resultado = [p for p in self._properties if p["ciudad"] == params.ciudad]
        
        if hasattr(params, "anio_construccion"):
            resultado = [p for p in self._properties if p["ciudad"] == params.anio_construccion]
            
        return list(resultado)
    
    def get_all(self):
        return list(self._properties)


class TestProperty:
    def test_get_property_without_params(self):
        property_repository = FakePropertyRepository()
        result_property = CreateProperty(property_repository).find_properties()

        assert len(result_property) == len(inmuebles)




    
