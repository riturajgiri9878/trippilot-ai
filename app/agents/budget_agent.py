from app.graph.state import TravelState
from app.models.results import BudgetResult


def budget_agent(state: TravelState) -> TravelState:
    request = state["request"]

    flight_cost = sum(flight.price for flight in state["flights"])

    stay_cost = sum(stay.total_price for stay in state["stays"])

    activity_cost = sum(
        activity.estimated_cost
        for activity in state["activities"]
    )

    total_cost = flight_cost + stay_cost + activity_cost

    remaining_budget = request.budget - total_cost

    budget_ratio = total_cost / request.budget

    if total_cost > request.budget:
        status = "OVER_BUDGET"
    elif budget_ratio >= 0.90:
        status = "NEAR_BUDGET"
    else:
        status = "WITHIN_BUDGET"

    state["budget"] = BudgetResult(
        flight_cost=flight_cost,
        stay_cost=stay_cost,
        activity_cost=activity_cost,
        total_cost=total_cost,
        user_budget=request.budget,
        remaining_budget=remaining_budget,
        status=status,
    )

    return state