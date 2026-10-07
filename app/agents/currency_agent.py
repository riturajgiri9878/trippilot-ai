from app.graph.state import TravelState
from app.tools.currency_tool import convert_currency


def currency_agent(
    state: TravelState,
) -> TravelState:
    request = state["request"]

    state["currency_conversion"] = (
        convert_currency(
            amount=request.budget,
            from_currency=request.currency,
            to_currency="USD",
        )
    )

    return state