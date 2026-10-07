from typing import Any, TypedDict

from app.models.results import (
    ActivityResult,
    BudgetResult,
    FlightResult,
    StayResult,
)
from app.models.trip import TripRequest


class TravelState(TypedDict):
    request: TripRequest

    flights: list[FlightResult]
    stays: list[StayResult]
    activities: list[ActivityResult]

    weather: dict[str, Any]
    budget: BudgetResult | None
    itinerary: list[dict[str, Any]]

    warnings: list[str]
    errors: list[dict[str, Any]]


def create_initial_state(request: TripRequest) -> TravelState:
    return {
        "request": request,
        "flights": [],
        "stays": [],
        "activities": [],
        "weather": {},
        "budget": None,
        "itinerary": [],
        "warnings": [],
        "errors": [],
    }