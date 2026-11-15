from typing import Any

from fastapi import APIRouter, HTTPException

from app.core.simulation import TelemetryUpdate, simulation_service

router = APIRouter(prefix="/api/v1", tags=["simulation"])


@router.get("/simulation/status")
async def get_simulation_status() -> dict[str, Any]:
    return simulation_service.status_snapshot()


@router.get("/simulation/scenarios")
async def list_scenarios() -> dict[str, Any]:
    return {"scenarios": simulation_service._scenario_list()}


@router.post("/simulation/scenarios/{scenario_id}/start")
async def start_scenario(scenario_id: str) -> dict[str, Any]:
    try:
        return await simulation_service.start_scenario(scenario_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/simulation/scenarios/{scenario_id}/pause")
async def pause_scenario(scenario_id: str) -> dict[str, Any]:
    try:
        if simulation_service.active_scenario != scenario_id and simulation_service.scenario_status != "paused":
            raise ValueError("The selected scenario is not currently active.")
        return await simulation_service.pause_scenario()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/simulation/scenarios/{scenario_id}/resume")
async def resume_scenario(scenario_id: str) -> dict[str, Any]:
    try:
        if simulation_service.active_scenario != scenario_id and simulation_service.scenario_status != "paused":
            raise ValueError("The selected scenario is not paused.")
        return await simulation_service.resume_scenario()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/simulation/stop")
async def stop_simulation() -> dict[str, Any]:
    return await simulation_service.stop_scenario()


@router.patch("/simulation/telemetry")
async def patch_telemetry(data: TelemetryUpdate) -> dict[str, Any]:
    return await simulation_service.patch_telemetry(data)


@router.post("/simulation/reset")
async def reset_simulation() -> dict[str, Any]:
    return await simulation_service.reset_simulation()


@router.get("/alerts")
async def list_alerts() -> dict[str, Any]:
    return {"alerts": simulation_service.list_alerts()}
