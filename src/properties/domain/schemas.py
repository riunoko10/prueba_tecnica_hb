from pydantic import BaseModel
from enum import Enum
from typing import Union


class PropertyState(Enum):
    PRE_VENTA = "pre_venta"
    EN_VENTA = "en_venta"
    VENDIDO = "vendido"

    @classmethod
    def _missing_(cls, value):
        raise ValueError(f"estado: '{value}' no válido. Estados permitidos: {', '.join([e.value for e in cls])}")

class PropertyRequest(BaseModel):
    anio: Union[str, None] = None
    ciudad: Union[str, None] = None
    estado: Union[str, None] = None

class PropertyResponse(BaseModel):
    direccion: str
    ciudad: str
    estado: str
    precio_venta: int
    descripcion: str
