from datetime import date
from typing import List

from pydantic import BaseModel, Field, field_validator, model_validator


class TripRequest(BaseModel):
    origin: str = Field(min_length=2, max_length=100)
    destination: str = Field(min_length=2, max_length=100)

    start_date: date
    end_date: date

    travelers: int = Field(ge=1, le=20)

    budget: float = Field(gt=0)

    currency: str = Field(default="INR", min_length=3, max_length=3)

    preferences: List[str] = Field(default_factory=list)

    @field_validator("origin", "destination")
    @classmethod
    def clean_location(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Location cannot be empty.")

        return cleaned

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("End date must be on or after start date.")

        return self