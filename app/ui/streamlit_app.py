import os
from datetime import date, timedelta

import httpx
import streamlit as st


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)


st.set_page_config(
    page_title="TripPilot AI",
    page_icon="✈️",
    layout="wide",
)


def call_trip_api(payload: dict) -> dict:
    response = httpx.post(
        f"{API_BASE_URL}/api/v1/trips/plan",
        json=payload,
        timeout=60.0,
    )

    response.raise_for_status()

    return response.json()


def format_money(
    amount,
    currency="INR",
):
    if amount is None:
        return "N/A"

    return f"{currency} {amount:,.2f}"


st.title("✈️ TripPilot AI")

st.write(
    "Multi-Agent AI Travel Planner"
)

st.info(
    "Flights, stays and activities currently use demo/mock data. "
    "Weather and currency services use live providers when available."
)


with st.sidebar:
    st.header("System")

    st.write(
        f"API: `{API_BASE_URL}`"
    )

    st.caption(
        "FastAPI backend must be running."
    )


with st.form(
    "trip_form",
):
    st.subheader("Plan your trip")

    col1, col2 = st.columns(2)

    with col1:
        origin = st.text_input(
            "Origin",
            value="Kolkata",
        )

        start_date = st.date_input(
            "Start date",
            value=date.today()
            + timedelta(days=30),
        )

        travelers = st.number_input(
            "Travelers",
            min_value=1,
            max_value=20,
            value=2,
            step=1,
        )

    with col2:
        destination = st.text_input(
            "Destination",
            value="Goa",
        )

        end_date = st.date_input(
            "End date",
            value=date.today()
            + timedelta(days=34),
        )

        budget = st.number_input(
            "Budget",
            min_value=1.0,
            value=30000.0,
            step=1000.0,
        )

    currency = st.selectbox(
        "Currency",
        options=[
            "INR",
            "USD",
            "EUR",
            "GBP",
        ],
        index=0,
    )

    preference_text = st.text_input(
        "Preferences",
        value="Beach, Food",
        help=(
            "Enter preferences separated "
            "by commas."
        ),
    )

    submitted = st.form_submit_button(
        "🚀 Plan My Trip",
        use_container_width=True,
    )


if submitted:
    preferences = [
        item.strip()
        for item in preference_text.split(",")
        if item.strip()
    ]

    payload = {
        "origin": origin,
        "destination": destination,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "travelers": int(travelers),
        "budget": float(budget),
        "currency": currency,
        "preferences": preferences,
    }

    with st.spinner(
        "TripPilot agents are planning your trip..."
    ):
        try:
            result = call_trip_api(
                payload
            )

            st.session_state[
                "trip_result"
            ] = result

        except httpx.HTTPStatusError as error:
            st.error(
                "Trip planning request failed."
            )

            try:
                st.json(
                    error.response.json()
                )
            except Exception:
                st.write(
                    error.response.text
                )

        except httpx.RequestError:
            st.error(
                "FastAPI backend is not reachable. "
                "Please make sure the API server "
                "is running on port 8000."
            )


result = st.session_state.get(
    "trip_result"
)


if result:
    trip_id = result.get(
        "trip_id"
    )

    status = result.get(
        "status",
        "UNKNOWN",
    )

    plan = result.get(
        "plan",
        {},
    )

    st.success(
        f"Trip #{trip_id} created successfully."
    )

    if status == "PLANNED":
        st.success(
            "Status: PLANNED"
        )
    else:
        st.warning(
            f"Status: {status}"
        )

    request_data = plan.get(
        "request",
        {},
    )

    flights = plan.get(
        "flights",
        [],
    )

    stays = plan.get(
        "stays",
        [],
    )

    activities = plan.get(
        "activities",
        [],
    )

    weather = plan.get(
        "weather",
        {},
    )

    currency_data = plan.get(
        "currency_conversion",
        {},
    )

    budget_data = plan.get(
        "budget",
    ) or {}

    itinerary = plan.get(
        "itinerary",
        [],
    )

    warnings = plan.get(
        "warnings",
        [],
    )

    errors = plan.get(
        "errors",
        [],
    )

    tab1, tab2, tab3, tab4, tab5 = (
        st.tabs(
            [
                "Overview",
                "Travel Options",
                "Weather & Currency",
                "Itinerary",
                "Diagnostics",
            ]
        )
    )

    with tab1:
        st.subheader(
            "Trip Overview"
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        with col1:
            st.metric(
                "Origin",
                request_data.get(
                    "origin",
                    origin,
                ),
            )

        with col2:
            st.metric(
                "Destination",
                request_data.get(
                    "destination",
                    destination,
                ),
            )

        with col3:
            st.metric(
                "Travelers",
                request_data.get(
                    "travelers",
                    travelers,
                ),
            )

        st.subheader(
            "Budget"
        )

        currency_code = request_data.get(
            "currency",
            currency,
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        with col1:
            st.metric(
                "Estimated Cost",
                format_money(
                    budget_data.get(
                        "total_cost"
                    ),
                    currency_code,
                ),
            )

        with col2:
            st.metric(
                "Budget",
                format_money(
                    budget_data.get(
                        "user_budget"
                    ),
                    currency_code,
                ),
            )

        with col3:
            st.metric(
                "Remaining",
                format_money(
                    budget_data.get(
                        "remaining_budget"
                    ),
                    currency_code,
                ),
            )

        st.write(
            "Budget status:",
            budget_data.get(
                "status",
                "Unknown",
            ),
        )

    with tab2:
        st.subheader(
            "Flights"
        )

        if flights:
            st.dataframe(
                flights,
                use_container_width=True,
            )
        else:
            st.warning(
                "No flight data available."
            )

        st.subheader(
            "Stays"
        )

        if stays:
            st.dataframe(
                stays,
                use_container_width=True,
            )
        else:
            st.warning(
                "No stay data available."
            )

        st.subheader(
            "Activities"
        )

        if activities:
            st.dataframe(
                activities,
                use_container_width=True,
            )
        else:
            st.warning(
                "No activity data available."
            )

    with tab3:
        st.subheader(
            "Live Weather"
        )

        if weather:
            col1, col2, col3 = (
                st.columns(3)
            )

            with col1:
                st.metric(
                    "Location",
                    weather.get(
                        "resolved_location",
                        "N/A",
                    ),
                )

            with col2:
                st.metric(
                    "Temperature",
                    (
                        f"{weather.get('temperature_c')} °C"
                        if weather.get(
                            "temperature_c"
                        )
                        is not None
                        else "N/A"
                    ),
                )

            with col3:
                st.metric(
                    "Feels Like",
                    (
                        f"{weather.get('feels_like_c')} °C"
                        if weather.get(
                            "feels_like_c"
                        )
                        is not None
                        else "N/A"
                    ),
                )

            st.caption(
                "Provider: "
                f"{weather.get('provider', 'Unknown')}"
            )

        else:
            st.warning(
                "Live weather currently unavailable."
            )

        st.subheader(
            "Currency Conversion"
        )

        if currency_data:
            st.write(
                f"{currency_data.get('original_amount')} "
                f"{currency_data.get('original_currency')}"
            )

            st.write("↓")

            st.write(
                f"{currency_data.get('converted_amount')} "
                f"{currency_data.get('converted_currency')}"
            )

            st.caption(
                "Provider: "
                f"{currency_data.get('provider', 'Unknown')}"
            )

        else:
            st.warning(
                "Currency conversion currently unavailable."
            )

    with tab4:
        st.subheader(
            "Suggested Itinerary"
        )

        if itinerary:
            for day in itinerary:
                with st.container(
                    border=True
                ):
                    st.write(
                        f"**Day {day.get('day', '')}**"
                    )

                    if day.get(
                        "date"
                    ):
                        st.caption(
                            day["date"]
                        )

                    st.write(
                        day
                    )

        else:
            st.warning(
                "No itinerary available."
            )

    with tab5:
        st.subheader(
            "System Diagnostics"
        )

        if warnings:
            for warning in warnings:
                st.warning(
                    warning
                )
        else:
            st.success(
                "No warnings."
            )

        if errors:
            st.error(
                "Some providers reported errors."
            )

            st.json(
                errors
            )
        else:
            st.success(
                "No agent errors."
            )