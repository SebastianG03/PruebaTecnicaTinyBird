from datetime import datetime
from typing import Optional

import pycountry
from pydantic import BaseModel, Field, field_validator


class MetricsEntry(BaseModel):
    country: Optional[str] = Field(description="Código ISO del país", examples=["CL", "AR", "BR"])
    from_date: Optional[str] = Field(description="Fecha inicial", examples=["2022-01-01T00:00:00Z"])
    to_date: Optional[str] = Field(description="Fecha final", examples=["2022-01-01T00:00:00Z"])

    @field_validator("country")
    def validate_country(cls, value: str) -> str:
        if value.strip():    
            try:
                pycountry.countries.lookup(value.upper().strip())
            except:
                raise ValueError("El código de país no es válido")

        return value.strip()

    @field_validator("from_date")
    def validate_from_date(cls, value: str) -> str:
        if value.strip():    
            try:
                datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
            except:
                raise ValueError("El formato de la fecha es incorrecto")

        return value
    
    @field_validator("to_date")
    def validate_to_date(cls, value: str) -> str:
        if value.strip():    
            try:
                datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
            except:
                raise ValueError("El formato de la fecha es incorrecto")

        return value