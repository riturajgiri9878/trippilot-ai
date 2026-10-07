import app.agents.weather_agent as weather_agent_module

from app.graph.state import create_initial_state
from app.models.trip import TripRequest


def test_weather_agent_uses_weather_tool(
    monkeypatch,
):
    fake_weather = {
        "requested_location": "Goa",
        "normalized_location": "Panjim, Goa",
        "resolved_location": "Panjim",
        "admin1": "Goa",
        "country": "India",
        "country_code": "IN",
        "latitude": 15.49574,
        "longitude": 73.82624,
        "temperature_c": 30.0,
        "provider": "open_meteo",
        "source_type": "live",
    }

    def fake_get_weather(
        location: str,
        country_code: str = "IN",
    ) -> dict:
        assert location == "Goa"
        assert country_code == "IN"

        return fake_weather

    monkeypatch.setattr(
        weather_agent_module,
        "get_weather",
        fake_get_weather,
    )

    trip = TripRequest(
        origin="Kolkata",
        destination="Goa",
        start_date="2026-12-10",
        end_date="2026-12-14",
        travelers=2,
        budget=30000,
        preferences=["Beach", "Food"],
    )

    state = create_initial_state(trip)

    result = weather_agent_module.weather_agent(
        state
    )

    assert result["weather"] == fake_weather
    assert (
        result["weather"]["resolved_location"]
        == "Panjim"
    )
    assert result["weather"]["admin1"] == "Goa"