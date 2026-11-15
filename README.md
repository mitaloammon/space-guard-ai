# Space Guard AI

A modular monolith foundation for the Space Guard AI mission assistant prototype.

## Technology baseline

- Python 3.12+
- FastAPI with Pydantic
- Vue 3 + TypeScript
- Vite
- Docker + Docker Compose

## Repository structure

- `docs/` contains the consolidated source-of-truth specification and the preserved legacy specification copy.
- `backend/` contains the Python FastAPI foundation.
- `frontend/` contains the Vue 3 + TypeScript foundation.
- `docker-compose.yml` provides the local development stack.

## Phase 1 and Phase 2 scope

This foundation includes:

- specification normalization
- project structure initialization
- backend foundation and health endpoints
- frontend foundation and JPL-inspired design language
- dependency configuration
- environment configuration
- Docker foundation

The full telemetry engine, deterministic safety rules, NASA data integrations, and AI assistant functionality remain out of scope for this phase.
