import pytest

import app.agents.currency_agent as currency_agent_module
import app.agents.weather_agent as weather_agent_module


@pytest.fixture(autouse=True)
def mock_external_services(monkeypatch):
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

    def fake_convert_currency(
        amount: float,
        from_currency: str,
        to_currency: str,
    ) -> dict:
        return {
            "original_amount": amount,
            "original_currency": from_currency,
            "converted_amount": 311.40,
            "converted_currency": to_currency,
            "rate": 0.01038,
            "rate_date": "2026-10-07",
            "provider": "frankfurter",
            "source_type": "live",
        }

    monkeypatch.setattr(
        weather_agent_module,
        "get_weather",
        fake_get_weather,
    )

    monkeypatch.setattr(
        currency_agent_module,
        "convert_currency",
        fake_convert_currency,
    )