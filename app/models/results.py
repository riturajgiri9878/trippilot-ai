from pydantic import BaseModel, Field


class FlightResult(BaseModel):
    airline: str
    origin: str
    destination: str

    departure_time: str
    arrival_time: str

    price: float = Field(ge=0)
    currency: str = "INR"

    provider: str
    source_type: str = "live"


class StayResult(BaseModel):
    property_name: str
    location: str

    price_per_night: float = Field(ge=0)
    total_price: float = Field(ge=0)

    currency: str = "INR"
    rating: float | None = Field(default=None, ge=0, le=5)

    provider: str
    source_type: str = "live"


class ActivityResult(BaseModel):
    name: str
    category: str
    location: str

    estimated_cost: float = Field(default=0, ge=0)
    estimated_duration_hours: float | None = Field(
        default=None,
        gt=0,
    )

    provider: str
    source_type: str = "live"
class BudgetResult(BaseModel):
    flight_cost: float = Field(ge=0)
    stay_cost: float = Field(ge=0)
    activity_cost: float = Field(ge=0)

    total_cost: float = Field(ge=0)

    user_budget: float = Field(gt=0)
    remaining_budget: float

    status: str