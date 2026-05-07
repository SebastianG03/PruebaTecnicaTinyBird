from datetime import datetime
from typing import Optional

from fastapi import HTTPException
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
                raise HTTPException(
                    detail="El código de país no es válido",
                    status_code=400
                )

        return value.strip()

    @field_validator("from_date")
    def validate_from_date(cls, value: str, info) -> str:
        if value.strip():    
            try:
                datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
            except:
                raise HTTPException(
                    detail="El formato de la fecha es incorrecto",
                    status_code=400
                )
            
            if datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ") > datetime.now():
                raise HTTPException(
                    detail="La fecha inicial no puede ser posterior a la fecha actual",
                    status_code=400
                )

            to_date = info.data.get("to_date")
            if to_date and datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ") > datetime.strptime(to_date, "%Y-%m-%dT%H:%M:%SZ"):
                raise HTTPException(
                    detail="La fecha inicial no puede ser posterior a la fecha final",
                    status_code=400
                )

        return value
    
    @field_validator("to_date")
    def validate_to_date(cls, value: str, info) -> str:
        
        if value.strip():    
            try:
                datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
            except:
                raise HTTPException(
                    detail="El formato de la fecha es incorrecto",
                    status_code=400
                )
            
            if datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ") > datetime.now():
                raise HTTPException(
                    detail="La fecha final no puede ser posterior a la fecha actual",
                    status_code=400
                )

            from_date = info.data.get("from_date")
            if from_date and datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ") < datetime.strptime(from_date, "%Y-%m-%dT%H:%M:%SZ"):
                raise HTTPException(
                    detail="La fecha final no puede ser anterior a la fecha inicial",
                    status_code=400
                )

        return value