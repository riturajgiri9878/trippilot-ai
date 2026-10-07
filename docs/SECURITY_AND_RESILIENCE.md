# TripPilot AI
## Security and Resilience Document

Version: 1.0
Project Type: Multi-Agent AI Travel Planner
Status: MVP

---

# 1. Purpose

This document defines the practical security, failure-handling,
fallback, backup, and recovery strategy for TripPilot AI.

The MVP will implement realistic protections without unnecessary
enterprise complexity.

---

# 2. Security Goals

TripPilot AI must:

- Protect API keys and secrets.
- Validate all external input.
- Prevent unauthorized access to saved trips.
- Restrict agent permissions.
- Handle prompt injection safely.
- Limit abusive requests.
- Avoid leaking technical errors or secrets.
- Use safe database operations.
- Continue operating during non-critical failures.

---

# 3. Threat Model

The MVP will protect against common realistic risks.

Examples:

- Invalid user input
- Excessive API requests
- Unauthorized trip access
- Prompt injection
- Secret leakage
- SQL injection
- External API failure
- LLM provider failure
- Corrupted or unavailable database
- Malformed provider responses

The MVP does not attempt to provide enterprise-grade protection
against every possible advanced attack.

---

# 4. Secret Management

Secrets include:

- LLM API keys
- Travel API credentials
- Database secrets
- Authentication secrets

Secrets must be stored in environment variables.

Local development:

.env

Example template:

.env.example

The real `.env` file must never be committed to Git.

Wrong:

```python
API_KEY = "my-secret-key"