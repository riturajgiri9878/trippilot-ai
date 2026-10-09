import app.services.trip_planner as trip_planner_module

from app.models.trip import TripRequest


def create_test_trip() -> TripRequest:
    return TripRequest(
        origin="Kolkata",
        destination="Goa",
        start_date="2026-12-10",
        end_date="2026-12-14",
        travelers=2,
        budget=30000,
        currency="INR",
        preferences=["Beach", "Food"],
    )


def test_complete_trip_planning_flow():
    trip = create_test_trip()

    result = trip_planner_module.plan_trip(trip)

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


def test_plan_trip_and_save(
    monkeypatch,
):
    class FakeSavedTrip:
        id = 99
        status = "PLANNED"

    captured = {}

    def fake_save_trip(
        request,
        plan_data=None,
        status="PLANNED",
    ):
        captured["request"] = request
        captured["plan_data"] = plan_data
        captured["status"] = status

        return FakeSavedTrip()

    monkeypatch.setattr(
        trip_planner_module,
        "save_trip",
        fake_save_trip,
    )

    trip = create_test_trip()

    trip_id, result = (
        trip_planner_module
        .plan_trip_and_save(trip)
    )

    assert trip_id == 99

    assert len(result["flights"]) == 1
    assert len(result["stays"]) == 1
    assert len(result["activities"]) == 1

    assert result["budget"] is not None
    assert result["budget"].total_cost == 15800

    assert len(result["itinerary"]) == 5

    assert captured["request"] == trip
    assert captured["plan_data"] == result
    assert captured["status"] == "PLANNED"