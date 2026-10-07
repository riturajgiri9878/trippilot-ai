import app.agents.currency_agent as currency_agent_module

from app.graph.state import create_initial_state
from app.models.trip import TripRequest


def test_currency_agent_uses_currency_tool(
    monkeypatch,
):
    fake_conversion = {
        "original_amount": 30000,
        "original_currency": "INR",
        "converted_amount": 311.40,
        "converted_currency": "USD",
        "rate": 0.01038,
        "rate_date": "2026-10-07",
        "provider": "frankfurter",
        "source_type": "live",
    }

    def fake_convert_currency(
        amount,
        from_currency,
        to_currency,
    ):
        assert amount == 30000
        assert from_currency == "INR"
        assert to_currency == "USD"

        return fake_conversion

    monkeypatch.setattr(
        currency_agent_module,
        "convert_currency",
        fake_convert_currency,
    )

    trip = TripRequest(
        origin="Kolkata",
        destination="Goa",
        start_date="2026-12-10",
        end_date="2026-12-14",
        travelers=2,
        budget=30000,
        currency="INR",
        preferences=["Beach", "Food"],
    )

    state = create_initial_state(trip)

    result = (
        currency_agent_module
        .currency_agent(state)
    )

    assert (
        result["currency_conversion"]
        == fake_conversion
    )

    assert (
        result["currency_conversion"]
        ["converted_currency"]
        == "USD"
    )