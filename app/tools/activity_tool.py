from app.models.results import ActivityResult
from app.models.trip import TripRequest


def search_activities(
    request: TripRequest,
) -> list[ActivityResult]:
    return [
        ActivityResult(
            name="Beach Sightseeing",
            category="Sightseeing",
            location=request.destination,
            estimated_cost=500,
            estimated_duration_hours=2,
            provider="local_mock",
            source_type="mock",
        )
    ]