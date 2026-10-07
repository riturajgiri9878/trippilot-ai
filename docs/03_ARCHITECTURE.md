# TripPilot AI
## System Architecture Document

Version: 1.0
Project Type: Multi-Agent AI Travel Planner
Architecture Style: Modular Monolith + Agent Orchestration
Status: MVP

---

# 1. Architecture Goals

TripPilot AI should be:

- Simple enough to build and understand.
- Modular enough to extend later.
- Resilient to external API failures.
- Secure with respect to secrets and user data.
- Cheap to run during development.
- Testable.
- Docker-ready.
- Resume and interview ready.

The MVP will avoid unnecessary microservices and distributed infrastructure.

---

# 2. Recommended Architecture

TripPilot AI will use a modular monolith architecture.

Main technologies:

Frontend:
- Streamlit

Backend:
- FastAPI

Agent Orchestration:
- LangGraph

Programming Language:
- Python

Validation:
- Pydantic

Database:
- SQLite for local MVP
- PostgreSQL-ready design for future deployment

Primary LLM:
- Gemini free-tier compatible model

Fallback LLM:
- Local Ollama/Qwen

Testing:
- pytest

Containerization:
- Docker

CI:
- GitHub Actions

---

# 3. High-Level Architecture

```text
                         USER
                           │
                           ▼
                    ┌──────────────┐
                    │  Streamlit   │
                    │   Frontend   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    │   Backend    │
                    └──────┬───────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │ Input Validation │
                 │    Pydantic      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    LangGraph     │
                 │   Orchestrator   │
                 └────────┬─────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Flight Agent │  │  Stay Agent  │  │Activity Agent│
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
 Flight Tool        Hotel Tool        Places Tool
       │                 │                 │
       ▼                 ▼                 ▼
 External API       External API       External API

        └─────────────────┼─────────────────┘
                          ▼
                 ┌──────────────────┐
                 │   Budget Logic   │
                 │     Python       │
                 └────────┬─────────┘
                          ▼
                 ┌──────────────────┐
                 │ Itinerary Agent  │
                 └────────┬─────────┘
                          ▼
                 ┌──────────────────┐
                 │   Final Result   │
                 └────────┬─────────┘
                          ▼
                      Database