from app.models.trip import TripRequest
from app.services.trip_planner import plan_trip


def test_complete_trip_planning_flow():
    trip = TripRequest(
        origin="Kolkata",
        destination="Goa",
        start_date="2026-12-10",
        end_date="2026-12-14",
        travelers=2,
        budget=30000,
        preferences=["Beach", "Food"],
    )

    result = plan_trip(trip)

    assert len(result["flights"]) == 1
    assert len(result["stays"]) == 1
    assert len(result["activities"]) == 1

    assert result["budget"] is not None
    assert result["budget"].total_cost == 15800
    assert result["budget"].remaining_budget == 14200
    assert result["budget"].status == "WITHIN_BUDGET"

    assert len(result["itinerary"]) == 5

    assert result["warnings"] == []
    assert result["errors"] == []