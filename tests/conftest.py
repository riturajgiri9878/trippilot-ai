import pytest

import app.agents.weather_agent as weather_agent_module


@pytest.fixture(autouse=True)
def mock_live_weather(monkeypatch):
    def fake_get_weather(
        location: str,
        country_code: str = "IN",
    ) -> dict:
        return {
            "requested_location": location,
            "normalized_location": "Panjim, Goa",
            "resolved_location": "Panjim",
            "admin1": "Goa",
            "country": "India",
            "country_code": country_code,
            "feature_code": "PPLA",
            "latitude": 15.49574,
            "longitude": 73.82624,
            "temperature_c": 30.0,
            "feels_like_c": 33.0,
            "precipitation_mm": 0.0,
            "weather_code": 1,
            "wind_speed_kmh": 5.0,
            "provider": "open_meteo",
            "source_type": "live",
        }

    monkeypatch.setattr(
        weather_agent_module,
        "get_weather",
        fake_get_weather,
    )