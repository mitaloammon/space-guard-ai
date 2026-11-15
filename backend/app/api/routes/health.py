from typing import Any

from fastapi import APIRouter

from app.core.simulation import simulation_service

router = APIRouter(tags=["foundation"])


@router.get("/health")
async def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "space-guard-ai",
        "phase": "foundation",
        "environment": "development",
        "checks": {
            "api": "ready",
            "simulation": "ready",
            "external_data": "mock_only",
            "ai_assistant": "mock_only",
        },
    }


@router.get("/api/v1/mission")
async def mission_status() -> dict[str, Any]:
    return {
        "mission_id": "mission-001",
        "status": "simulator-ready",
        "target_body": "Mars",
        "phase": "system_bootstrap",
        "telemetry_source": "simulated",
        "external_data_status": "mock_only",
    }


@router.get("/api/v1/mission/status")
async def mission_status_alias() -> dict[str, Any]:
    return await mission_status()


@router.get("/api/v1/telemetry/current")
async def telemetry_status() -> dict[str, Any]:
    return {"telemetry": simulation_service.status_snapshot()["telemetry"]}
