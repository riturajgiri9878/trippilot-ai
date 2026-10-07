# TripPilot AI
## Product Requirements Document (PRD)

Version: 1.0  
Project Type: Multi-Agent AI Travel Planner  
Status: MVP Planning

---

# 1. Product Overview

TripPilot AI is a multi-agent travel planning application that helps users
create personalized travel plans based on destination, dates, budget,
number of travelers, and interests.

Instead of using one AI model for every task, TripPilot AI uses specialized
agents for flights, stays, activities, budget validation, and itinerary
generation.

The system combines the results of these agents and produces a structured
day-wise travel plan.

---

# 2. Problem Statement

Planning a trip usually requires users to search across multiple platforms
for:

- Flights
- Hotels
- Activities
- Weather
- Currency information
- Budget calculations
- Daily itinerary planning

This process is time-consuming and fragmented.

Users may also struggle to determine whether the complete trip fits within
their available budget.

TripPilot AI aims to reduce this effort by coordinating specialized AI agents
and external APIs through a single application.

---

# 3. Target Users

The MVP is designed for:

- Solo travelers
- Couples
- Families
- Students
- Budget-conscious travelers
- Users who want fast AI-assisted trip planning

The system is intended for travel planning and recommendations.

It is not intended to act as a booking or payment platform in the MVP.

---

# 4. Product Goals

The primary goals of TripPilot AI are:

1. Generate personalized travel plans.

2. Coordinate multiple specialized AI agents.

3. Retrieve available travel-related information from external APIs.

4. Keep recommendations within the user's budget where possible.

5. Generate a clear day-wise itinerary.

6. Continue operating when a non-critical API or agent fails.

7. Protect API keys and user information.

8. Use free-tier APIs and local AI models during development whenever possible.

---

# 5. Core Multi-Agent System

TripPilot AI will contain the following major agents.

## Orchestrator Agent

Coordinates the complete workflow.

Responsibilities:

- Receive validated trip requirements.
- Decide which agents need to run.
- Collect agent outputs.
- Handle partial failures.
- Send results to the itinerary generation process.

---

## Flight Agent

Responsible for:

- Searching available flight information.
- Returning structured flight options.
- Handling unavailable flight providers.

---

## Stay Agent

Responsible for:

- Finding suitable accommodation.
- Considering destination and trip dates.
- Returning structured stay recommendations.

---

## Activity Agent

Responsible for:

- Finding attractions and activities.
- Matching activities with user interests.
- Returning destination-based recommendations.

---

## Budget Agent

Responsible for:

- Calculating estimated trip cost.
- Comparing estimated cost against the user's budget.
- Identifying budget overruns.

Financial calculations must be performed using deterministic application
logic rather than relying only on the LLM.

---

## Itinerary Agent

Responsible for:

- Combining flights, stays, activities, and budget information.
- Creating a day-wise travel schedule.
- Providing the final user-friendly travel plan.

---

# 6. MVP User Input

The application must allow the user to provide:

- Origin
- Destination
- Start date
- End date
- Number of travelers
- Total budget
- Travel interests/preferences

Optional preferences may include:

- Food
- Adventure
- Sightseeing
- Culture
- Shopping
- Nature

---

# 7. MVP Output

The system should generate:

- Trip summary
- Suggested flight options
- Suggested accommodation
- Recommended activities
- Estimated trip cost
- Budget status
- Day-wise itinerary
- Important warnings
- Information about unavailable services

---

# 8. Reliability and Failover

TripPilot AI must not completely fail because one external service is
temporarily unavailable.

The system will follow a simple fallback strategy.

Example:

Primary Flight API
→ if successful, use live/test data
→ if unavailable, use cached or mock data
→ inform the user when fallback data is being used

For AI models:

Primary AI Model
→ Gemini free tier

Fallback AI Model
→ Local Ollama/Qwen model

The system should provide partial results whenever possible instead of
failing the entire trip planning request.

---

# 9. Security Requirements

The MVP will implement practical security controls without unnecessary
enterprise complexity.

The application must:

- Store API keys in environment variables.
- Never commit `.env` files to Git.
- Validate user input.
- Restrict agent access to approved tools only.
- Avoid exposing secrets through LLM prompts or logs.
- Use safe database queries.
- Apply authorization to saved user trips.
- Implement basic rate limiting.
- Handle malicious or invalid input safely.

Agents must follow the principle of least privilege.

For example, the Flight Agent should be able to search flight information
but must not have permission to execute operating system commands or delete
database records.

---

# 10. Backup and Recovery

The system will maintain a simple backup strategy.

During local development:

Primary Database:
SQLite

Backup:
Periodic SQLite database copy

The project will provide backup and restore scripts.

Example:

scripts/backup_db.py

scripts/restore_db.py

For future production deployment, PostgreSQL and managed backups may replace
the local SQLite system.

---

# 11. MVP Scope

The first working version will include:

User travel request
→ Input validation
→ Shared travel state
→ Multi-agent orchestration
→ Flight search
→ Stay search
→ Activity search
→ Budget calculation
→ Day-wise itinerary
→ Error handling
→ API fallback
→ Database storage
→ Basic security
→ Automated testing
→ Docker support
→ GitHub Actions CI
→ Deployment

---

# 12. Out of Scope for MVP

The following features will not be implemented in the initial MVP:

Real flight booking

Real hotel booking

Payment processing

Credit card storage

Travel insurance purchasing

Visa application processing

Complex enterprise infrastructure

Kubernetes

Kafka

Microservice architecture

Blockchain

Advanced recommendation training pipelines

Native Android or iOS applications

These features may be considered for future versions.

---

# 13. User Stories

## User Story 1

As a traveler,
I want to enter my destination, dates, and budget,
so that I can receive a personalized travel plan.

Acceptance:

The system accepts valid trip information and starts the planning workflow.

---

## User Story 2

As a traveler,
I want flight and stay recommendations,
so that I do not need to search multiple websites manually.

Acceptance:

The system returns available options or clearly reports provider
unavailability.

---

## User Story 3

As a traveler,
I want activities based on my interests,
so that my itinerary matches my preferences.

Acceptance:

Recommended activities should be related to the destination and selected
interests.

---

## User Story 4

As a budget-conscious traveler,
I want to know the estimated total cost,
so that I can understand whether the trip fits my budget.

Acceptance:

The system calculates estimated cost and displays whether the trip is
within or over budget.

---

## User Story 5

As a traveler,
I want the application to continue working if one external service fails,
so that I can still receive a useful travel plan.

Acceptance:

A non-critical provider failure must not crash the complete planning
workflow.

---

# 14. Success Metrics

The MVP will be considered successful when:

A valid travel request can complete the full planning workflow.

The system generates a structured itinerary.

Budget calculations are deterministic and correct.

At least one external provider can fail without crashing the application.

The backup AI model can be used when the primary AI model is unavailable.

Invalid inputs are rejected correctly.

Critical functionality is covered by automated tests.

The application can run through Docker.

GitHub Actions automatically runs the test suite.

---

# 15. Assumptions

The MVP assumes:

Free APIs may have usage limits.

Some free travel APIs may provide test or limited data.

Prices may not represent real-time booking prices.

Internet access is required for external APIs.

A local AI model may provide lower-quality responses than the primary model.

The system provides planning assistance rather than guaranteed booking
information.

---

# 16. Risks

## External API Limits

Free API quota may be exhausted.

Mitigation:

Use caching, controlled API calls, and fallback data.

---

## API Provider Failure

A provider may become unavailable.

Mitigation:

Use timeouts, limited retries, and fallback providers/data.

---

## LLM Failure

Primary LLM may fail because of quota or service problems.

Mitigation:

Use local Ollama/Qwen as the fallback model.

---

## Hallucinated Information

LLMs may generate incorrect travel information.

Mitigation:

Use external API data for factual information and deterministic Python
logic for calculations.

---

## Security Risks

Attackers may attempt excessive requests, malicious input, prompt injection,
or unauthorized access.

Mitigation:

Validation, rate limiting, authorization, limited agent tools, secure secret
management, and logging.

---

# 17. Acceptance Criteria

The MVP is complete when:

1. User can submit a valid travel request.

2. Invalid requests are rejected with understandable errors.

3. Orchestrator can coordinate specialist agents.

4. Flight Agent can return flight information or fallback data.

5. Stay Agent can return accommodation information or fallback data.

6. Activity Agent can return destination activities.

7. Budget Agent calculates estimated total cost correctly.

8. Itinerary Agent creates a structured day-wise plan.

9. Application survives failure of a non-critical agent or API.

10. API keys are not stored in source code.

11. Database information can be backed up and restored.

12. Core functionality has automated tests.

13. Project runs successfully through Docker.

14. GitHub Actions executes tests automatically.

15. README explains installation, architecture, usage, and limitations.

---

# 18. MVP Definition

TripPilot AI MVP is a secure and resilient multi-agent travel planning
application capable of generating a personalized travel itinerary while
using free or test APIs, deterministic budget calculations, graceful
fallbacks, and a local AI backup model.