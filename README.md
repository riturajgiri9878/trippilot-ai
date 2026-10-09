# ✈️ TripPilot AI

TripPilot AI is a multi-agent travel planning application built with Python, LangGraph, FastAPI, Streamlit, SQLAlchemy, Docker, and GitHub Actions.

The system coordinates multiple specialized agents to create a travel plan including flights, stays, activities, weather, currency conversion, budget analysis, and a day-wise itinerary.

---

## 🚀 Features

- Multi-agent travel planning workflow
- Flight Agent
- Stay Agent
- Activity Agent
- Weather Agent
- Currency Agent
- Budget Agent
- Itinerary Agent
- LangGraph-based orchestration
- FastAPI REST API
- Streamlit user interface
- SQLite trip persistence
- Provider failure handling
- Flight fallback mechanism
- Dockerized backend and frontend
- GitHub Actions CI
- Automated pytest test suite

---

## 🧠 Architecture

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
FastAPI
 │
 ▼
Trip Planner Service
 │
 ▼
LangGraph
 │
 ├── Flight Agent
 ├── Stay Agent
 ├── Activity Agent
 ├── Weather Agent
 ├── Currency Agent
 ├── Budget Agent
 └── Itinerary Agent
 │
 ▼
SQLite Database