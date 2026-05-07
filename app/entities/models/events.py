from datetime import datetime
from re import L

from pydantic import field_validator
from sqlmodel import SQLModel, Field
import pycountry

from app.entities.types.event_type import EventTypes

class Events(SQLModel, table=True):
    event_id: str = Field(primary_key=True, index=True, unique=True, description="El id del evento")
    user_id: str = Field(index=True, include="u_", regex="u_[0-9]+", description="El id del usuario")
    event_type: EventTypes = Field(description="El tipo de evento")
    product_id: str = Field(index=True, include="p_", regex="p_[0-9]+", description="El id del producto")
    timestamp: str = Field(regex=r'^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])T([01]\d|2[0-3]):([0-5]\d):([0-5]\d)Z$', description="La fecha y hora del evento")
    price: float = Field(decimal_places=2, ge=0, description="El precio del producto")
    country: str = Field(min_length=2, description="Código ISO del país")

    @field_validator("timestamp")
    def validate_timestamp(cls, value: str) -> str:
        if not value:
            raise ValueError("Timestamp no puede estar vacío")
        
        timestamps = value.split("T")

        if len(timestamps) != 2:
            raise ValueError("El formato de la fecha es incorrecto")
        
        date = timestamps[0].split("-")

        if len(date) != 3:
            raise ValueError("El formato de la fecha es incorrecto")
        
        year, month, day = date[0].strip(), date[1].strip(), date[2].strip()
        
        if not year.isnumeric() or not month.isnumeric() or not day.isnumeric():
            raise ValueError("El formato de la fecha es incorrecto")
        
        year, month, day = int(year), int(month), int(day)

        try:
            datetime(year, month, day)
        except ValueError:
            raise ValueError("El formato de la fecha es incorrecto")

        time = timestamps[1].split(":")
        
        if len(time) != 3:
            raise ValueError("El formato de la fecha es incorrecto")
        
        hour, minute, second = time[0].strip(), time[1].strip(), time[2].strip()
        
        if not hour.isnumeric() or not minute.isnumeric() or not second.isnumeric():
            raise ValueError("El formato de la fecha es incorrecto")
        
        hour, minute, second = int(hour), int(minute), int(second)

        try:
            datetime(year, month, day, hour, minute, second)
        except ValueError:
            raise ValueError("El formato de la fecha es incorrecto")

        return value.strip()

    @field_validator("price")
    def validate_price(cls, value: float) -> float:
        if value < 0:
            raise ValueError("El precio no puede ser negativo")
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
        
        try:
            return EventTypes(value.upper().strip())
        except ValueError:
            raise ValueError("El tipo de evento no es válido")
