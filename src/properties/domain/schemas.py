from pydantic import BaseModel
from enum import Enum
from typing import Optional, Union


class PropertyState(Enum):
    PRE_VENTA = "pre_venta"
    EN_VENTA = "en_venta"
    VENDIDO = "vendido"

class PropertyRequest(BaseModel):
    anio_construcion: Union[str, None] = None
    ciudad: Union[str, None] = None
    estado: Union[PropertyState, None] = None

class PropertyResponse(BaseModel):
    direccion: str
    ciudad: str
    estado: str
    precio_venta: int
    descripcion: str
