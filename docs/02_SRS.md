# TripPilot AI
## Software Requirements Specification (SRS)

Version: 1.0
Project Type: Multi-Agent AI Travel Planner
Status: MVP

---

# 1. Purpose

This document defines the functional and non-functional requirements for
TripPilot AI.

TripPilot AI is a multi-agent travel planning system that coordinates
specialized agents for flights, stays, activities, budget validation, and
itinerary generation.

The MVP will use free-tier, test, or local services whenever possible.

---

# 2. System Objectives

The system must:

1. Accept structured travel requirements.
2. Validate user input.
3. Coordinate multiple specialized agents.
4. Retrieve travel-related information from external APIs.
5. Calculate estimated travel costs using deterministic code.
6. Generate a day-wise itinerary.
7. Handle API and agent failures gracefully.
8. Protect secrets and user data.
9. Support backup and recovery.
10. Remain usable when non-critical services fail.

---

# 3. User Roles

## 3.1 Guest User

A guest user may:

- Enter trip details.
- Generate a travel plan.
- View recommendations.

A guest user will not have persistent trip history.

---

## 3.2 Registered User

A registered user may:

- Generate travel plans.
- Save trips.
- View their own saved trips.
- Delete their own saved trips.

A registered user must not access another user's saved trips.

---

# 4. Functional Requirements

## FR-01: Trip Request

The system shall allow the user to enter:

- Origin
- Destination
- Start date
- End date
- Number of travelers
- Total budget
- Travel interests

---

## FR-02: Input Validation

The system shall validate all trip requests before running agents.

The request shall be rejected when:

- Origin is empty.
- Destination is empty.
- Start date is after end date.
- Number of travelers is less than 1.
- Budget is zero or negative.
- Required data is missing.

Invalid requests must not start the agent workflow.

---

## FR-03: Orchestrator Agent

The Orchestrator Agent shall:

- Receive validated travel requirements.
- Create the shared travel state.
- Trigger required specialist agents.
- Collect their outputs.
- Record agent failures.
- Continue processing when a non-critical agent fails.
- Pass the collected state to final itinerary generation.

---

## FR-04: Flight Agent

The Flight Agent shall:

- Receive origin, destination, travel dates, and traveler count.
- Call the configured flight provider.
- Return structured flight options.

Each flight result should contain, when available:

- Airline
- Origin
- Destination
- Departure time
- Arrival time
- Price
- Currency
- Provider
- Data source type

The Flight Agent must not invent live prices.

---

## FR-05: Flight Fallback

If the primary flight provider fails:

1. Retry only according to configured retry rules.
2. Attempt the fallback provider or fallback data.
3. Mark the returned data as fallback data.
4. Record the primary provider failure.

The application must not crash solely because the flight provider is unavailable.

---

## FR-06: Stay Agent

The Stay Agent shall:

- Search accommodation for the destination.
- Use trip dates and traveler count.
- Return structured stay options.

Each stay result should contain, when available:

- Property name
- Location
- Price
- Currency
- Rating
- Provider
- Data source type

---

## FR-07: Activity Agent

The Activity Agent shall:

- Search destination activities.
- Consider selected user interests.
- Return relevant activities.

Activity output may contain:

- Activity name
- Category
- Location
- Estimated duration
- Estimated cost
- Provider

---

## FR-08: Weather Information

The system may retrieve weather information for the destination.

Weather data should be used to improve itinerary recommendations.

Failure of the weather API must not stop trip generation.

---

## FR-09: Currency Conversion

When travel data uses different currencies, the system should convert
financial values into a common currency when conversion information is
available.

Currency API failure must not crash the application.

---

## FR-10: Budget Agent

The Budget Agent shall calculate:

- Flight cost
- Stay cost
- Activity cost
- Estimated total cost
- Remaining budget or budget excess

Budget calculations must use deterministic Python logic.

The LLM must not be treated as the source of truth for financial calculations.

---

## FR-11: Budget Status

The system shall classify a generated trip as:

- WITHIN_BUDGET
- NEAR_BUDGET
- OVER_BUDGET

The exact threshold for NEAR_BUDGET shall be configurable.

---

## FR-12: Itinerary Agent

The Itinerary Agent shall generate a day-wise travel plan.

The itinerary should contain:

- Day number
- Date
- Recommended activities
- Stay information
- Relevant travel information
- Warnings if applicable

---

## FR-13: Partial Results

If one non-critical service fails, the system should return all successfully
generated information.

Example:

Flights: unavailable
Hotels: available
Activities: available
Itinerary: available with warning

---

## FR-14: Saved Trips

Registered users shall be able to save completed trips.

Each saved trip must be associated with the authenticated user's ID.

---

## FR-15: Trip History

Registered users shall be able to retrieve their own saved trips.

The system must prevent access to trips belonging to other users.

---

# 5. Shared Travel State

The multi-agent system shall use a shared state.

Example structure:

```python
{
    "request": {},
    "flights": [],
    "stays": [],
    "activities": [],
    "weather": {},
    "budget": {},
    "itinerary": [],
    "warnings": [],
    "errors": []
}