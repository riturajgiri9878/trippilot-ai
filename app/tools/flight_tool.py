from app.models.results import FlightResult
from app.models.trip import TripRequest


def search_primary_flights(request: TripRequest) -> list[FlightResult]:
    return [
        FlightResult(
            airline="Mock Airways",
            origin=request.origin,
            destination=request.destination,
            departure_time="08:30",
            arrival_time="11:15",
            price=6500,
            currency=request.currency,
            provider="mock_primary",
            source_type="mock",
        )
    ]


def search_fallback_flights(request: TripRequest) -> list[FlightResult]:
    return [
        FlightResult(
            airline="Fallback Airways",
            origin=request.origin,
            destination=request.destination,
            departure_time="09:00",
            arrival_time="12:00",
            price=6500,
            currency=request.currency,
            provider="local_fallback",
            source_type="fallback",
        )
    ]