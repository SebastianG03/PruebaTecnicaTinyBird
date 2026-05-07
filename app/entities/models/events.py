from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator
import pycountry

from app.entities.types.event_type import EventTypes

class Events(BaseModel):
    event_id: str = Field(description="El id del evento")
    user_id: str = Field(description="El id del usuario")
    event_type: str = Field(description="El tipo de evento")
    product_id: str = Field(description="El id del producto")
    timestamp: str = Field(description="La fecha y hora del evento")
    price: float = Field(ge=0.00, description="El precio del producto")
    country: str = Field(min_length=2, description="Código ISO del país")

    @field_validator("timestamp")
    def validate_timestamp(cls, value: str) -> str:
        if not value:
            raise ValueError("Timestamp no puede estar vacío")
        
        formats = [
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S%z",
            ]
        
        for format in formats:
            try:
                datetime.strptime(value, format)
                return value
            except:
                pass

        raise ValueError("El formato de la fecha es incorrecto")

    @field_validator("price")
    def validate_price(cls, value: float, info) -> float:
        if value < 0:
            raise ValueError("El precio no puede ser negativo")
        
        event_type = info.data.get("event_type")
        if event_type == EventTypes.PURCHASE and value == 0:
            raise ValueError("El precio no puede ser 0 para un evento de compra")

        return value
    
    @field_validator("event_id")
    def validate_event_id(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El id no puede estar vacío")
        
        if not value.startswith("evt_"):
            raise ValueError("El id debe comenzar con 'evt_'")
        
        numeric_section = value.split("_")[1]

        if not numeric_section.isnumeric() or len(numeric_section) < 3:
            raise ValueError("El id debe comenzar con 'evt_' seguido de un número de 3 o más dígitos")

        return value.strip()
    
    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El id no puede estar vacío")
        
        if not value.startswith("u_"):
            raise ValueError("El id debe comenzar con 'u_'")
        
        numeric_section = value.split("_")[1]

        if not numeric_section.isnumeric() or len(numeric_section) < 3:
            raise ValueError("El id debe comenzar con 'u_' seguido de un número de 3 o más dígitos")

        return value.strip()
    
    @field_validator("product_id")
    def validate_product_id(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El id no puede estar vacío")
        
        if not value.startswith("p_"):
            raise ValueError("El id debe comenzar con 'p_'")
        
        numeric_section = value.split("_")[1]

        if not numeric_section.isnumeric():
            raise ValueError("El id debe comenzar con 'p_' seguido de un número de 1 o más dígitos")

        return value.strip()
    
    @field_validator("country")
    def validate_country(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El código de país no puede estar vacío")
        
        try:
            country = pycountry.countries.lookup(value.upper().strip())
        except:
            raise ValueError("El código de país no es válido")

        return value.strip()


    @field_validator("event_type")
    def validate_event_type(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El tipo de evento no puede estar vacío")
        
        if not value in EventTypes.__members__.values() or not value in EventTypes:
            raise ValueError("El tipo de evento no es válido")

        return value
