from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.config import settings
from app.core.websocket_manager import websocket_manager

TelemetryStatus = Literal["connected", "disconnected"]
AlertSeverity = Literal["warning", "critical"]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class TelemetryUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    oxygen: float | None = Field(default=None, ge=0.0, le=100.0)
    pressure_psi: float | None = Field(default=None, ge=0.0, le=20.0)
    temperature_celsius: float | None = Field(default=None, ge=-80.0, le=120.0)
    battery_level: float | None = Field(default=None, ge=0.0, le=100.0)
    radiation_rate_msv_h: float | None = Field(default=None, ge=0.0, le=25.0)
    communication_status: TelemetryStatus | None = None

    @field_validator("communication_status")
    @classmethod
    def validate_status(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if value not in {"connected", "disconnected"}:
            raise ValueError("communication_status must be 'connected' or 'disconnected'")
        return value


class SimulationService:
    _scenario_catalog: dict[str, dict[str, Any]] = {
        "normal_operation": {
            "name": "Normal Operation",
            "description": "All telemetry values remain inside the configured demonstration thresholds.",
            "progressive": False,
        },
        "low_oxygen": {
            "name": "Low Oxygen",
            "description": "Reduce the simulated oxygen reserve to trigger the oxygen alarm.",
            "progressive": True,
        },
        "pressure_anomaly": {
            "name": "Pressure Anomaly",
            "description": "Reduce suit pressure to simulate a pressure loss condition.",
            "progressive": True,
        },
        "high_temperature": {
            "name": "High Temperature",
            "description": "Increase suit temperature to trigger a heat warning.",
            "progressive": True,
        },
        "low_battery": {
            "name": "Low Battery",
            "description": "Reduce battery capacity to replicate a system power risk.",
            "progressive": True,
        },
        "radiation_increase": {
            "name": "Radiation Increase",
            "description": "Increase radiation rate to trigger the radiation safety alert.",
            "progressive": True,
        },
        "communication_loss": {
            "name": "Communication Loss",
            "description": "Disconnect the simulated comms link to represent a loss of contact.",
            "progressive": False,
        },
    }

    def __init__(self) -> None:
        self.mission_id = "mission-001"
        self._lock = asyncio.Lock()
        self._telemetry: dict[str, Any] = self._baseline_telemetry()
        self._baseline: dict[str, Any] = self._baseline_telemetry()
        self.mode: str = "manual"
        self.active_scenario: str | None = None
        self.scenario_status: str = "idle"
        self.execution_start_time: str | None = None
        self.alerts: list[dict[str, Any]] = []
        self._scenario_task: asyncio.Task[Any] | None = None
        self._scenario_step = 0
        self._evaluate_alerts()

    def _baseline_telemetry(self) -> dict[str, Any]:
        return {
            "oxygen": 86.0,
            "pressure_psi": 4.3,
            "temperature_celsius": 28.1,
            "battery_level": 62.0,
            "radiation_rate_msv_h": 0.42,
            "communication_status": "connected",
        }

    def _thresholds(self) -> dict[str, Any]:
        return {
            "oxygen_warning": 75.0,
            "oxygen_critical": 50.0,
            "pressure_warning": 3.5,
            "temperature_warning": 33.0,
            "temperature_critical": 37.0,
            "battery_warning": 25.0,
            "radiation_warning": 1.4,
            "radiation_critical": 2.0,
            "demonstration_only": True,
        }

    def _scenario_list(self) -> list[dict[str, Any]]:
        return [
            {
                "id": scenario_id,
                "name": scenario["name"],
                "description": scenario["description"],
                "progressive": scenario.get("progressive", False),
            }
            for scenario_id, scenario in self._scenario_catalog.items()
        ]

    def _apply_scenario_values(self, scenario_id: str, step: int) -> dict[str, Any]:
        values = self._baseline_telemetry()
        if scenario_id == "normal_operation":
            return values
        if scenario_id == "low_oxygen":
            values["oxygen"] = max(30.0, 86.0 - (step * 7.0))
            values["temperature_celsius"] = 29.0
            return values
        if scenario_id == "pressure_anomaly":
            values["pressure_psi"] = max(1.2, 4.3 - (step * 0.7))
            return values
        if scenario_id == "high_temperature":
            values["temperature_celsius"] = min(50.0, 28.1 + (step * 2.5))
            return values
        if scenario_id == "low_battery":
            values["battery_level"] = max(5.0, 62.0 - (step * 9.0))
            return values
        if scenario_id == "radiation_increase":
            values["radiation_rate_msv_h"] = min(8.0, 0.42 + (step * 0.6))
            return values
        if scenario_id == "communication_loss":
            values["communication_status"] = "disconnected"
            return values
        return values

    def _rule_alerts(self) -> list[dict[str, Any]]:
        telemetry = self._telemetry
        thresholds = self._thresholds()
        alerts: list[dict[str, Any]] = []

        if telemetry["oxygen"] <= thresholds["oxygen_critical"]:
            alerts.append(
                {
                    "id": "alert-low-oxygen",
                    "alert_type": "low_oxygen",
                    "severity": "critical",
                    "description": "Oxygen has fallen below the configured demonstration threshold.",
                    "telemetry_parameter": "oxygen",
                }
            )
        elif telemetry["oxygen"] <= thresholds["oxygen_warning"]:
            alerts.append(
                {
                    "id": "alert-low-oxygen",
                    "alert_type": "low_oxygen",
                    "severity": "warning",
                    "description": "Oxygen is approaching the configured demonstration threshold.",
                    "telemetry_parameter": "oxygen",
                }
            )

        if telemetry["pressure_psi"] <= thresholds["pressure_warning"]:
            alerts.append(
                {
                    "id": "alert-pressure-anomaly",
                    "alert_type": "pressure_anomaly",
                    "severity": "warning",
                    "description": "Suit pressure is below the configured demonstration threshold.",
                    "telemetry_parameter": "pressure_psi",
                }
            )

        if telemetry["temperature_celsius"] >= thresholds["temperature_warning"]:
            severity = "critical" if telemetry["temperature_celsius"] >= thresholds["temperature_critical"] else "warning"
            alerts.append(
                {
                    "id": "alert-high-temperature",
                    "alert_type": "high_temperature",
                    "severity": severity,
                    "description": "Temperature exceeds the configured demonstration threshold.",
                    "telemetry_parameter": "temperature_celsius",
                }
            )

        if telemetry["battery_level"] <= thresholds["battery_warning"]:
            alerts.append(
                {
                    "id": "alert-low-battery",
                    "alert_type": "low_battery",
                    "severity": "warning",
                    "description": "Battery is below the configured demonstration threshold.",
                    "telemetry_parameter": "battery_level",
                }
            )

        if telemetry["radiation_rate_msv_h"] >= thresholds["radiation_warning"]:
            severity = "critical" if telemetry["radiation_rate_msv_h"] >= thresholds["radiation_critical"] else "warning"
            alerts.append(
                {
                    "id": "alert-radiation-increase",
                    "alert_type": "radiation_increase",
                    "severity": severity,
                    "description": "Radiation rate exceeds the configured demonstration threshold.",
                    "telemetry_parameter": "radiation_rate_msv_h",
                }
            )

        if telemetry["communication_status"] == "disconnected":
            alerts.append(
                {
                    "id": "alert-communication-loss",
                    "alert_type": "communication_loss",
                    "severity": "warning",
                    "description": "Communication has been intentionally disconnected in the simulation.",
                    "telemetry_parameter": "communication_status",
                }
            )

        return alerts

    def _make_alert_id(self, alert_type: str) -> str:
        return f"{self.mission_id}:{alert_type}"

    def _evaluate_alerts(self) -> None:
        current_rules = self._rule_alerts()
        rule_types = {alert["alert_type"] for alert in current_rules}
        resolved_history: list[dict[str, Any]] = []
        existing_active: dict[str, dict[str, Any]] = {}

        for alert in self.alerts:
            alert_type = alert.get("alert_type")
            if alert.get("status") == "active":
                if alert_type in rule_types:
                    existing_active[alert_type] = alert
                else:
                    alert["status"] = "resolved"
                    alert["resolved_at"] = utc_now_iso()
                    resolved_history.append(alert)
                    continue
            resolved_history.append(alert)

        next_alerts: list[dict[str, Any]] = list(resolved_history)
        for alert in current_rules:
            alert_type = alert["alert_type"]
            alert_id = self._make_alert_id(alert_type)
            current = existing_active.get(alert_type)
            if current is not None:
                current["id"] = alert_id
                current["alert_id"] = alert_id
                current["mission_id"] = self.mission_id
                current["severity"] = alert["severity"]
                current["description"] = alert["description"]
                current["telemetry_parameter"] = alert["telemetry_parameter"]
                current["status"] = "active"
                current["updated_at"] = utc_now_iso()
                current["source"] = "safety_rules_engine"
                current["acknowledged"] = bool(current.get("acknowledged", False))
                next_alerts.append(current)
                continue

            alert_payload = {
                **alert,
                "id": alert_id,
                "alert_id": alert_id,
                "mission_id": self.mission_id,
                "status": "active",
                "timestamp": utc_now_iso(),
                "source": "safety_rules_engine",
                "acknowledged": False,
            }
            next_alerts.append(alert_payload)

        deduped_alerts: list[dict[str, Any]] = []
        seen_active: set[str] = set()
        for alert in next_alerts:
            alert_type = alert.get("alert_type")
            if alert.get("status") == "active":
                if alert_type in seen_active:
                    continue
                seen_active.add(alert_type)
            deduped_alerts.append(alert)

        self.alerts = sorted(deduped_alerts, key=lambda item: item.get("timestamp", ""), reverse=True)

    async def _emit_event(self, event_type: str, data: dict[str, Any]) -> None:
        await websocket_manager.broadcast({
            "type": event_type,
            "timestamp": utc_now_iso(),
            "data": data,
        })

    async def _scenario_loop(self, scenario_id: str) -> None:
        while self.active_scenario == scenario_id and self.scenario_status == "running":
            await asyncio.sleep(2.0)
            self._scenario_step += 1
            async with self._lock:
                self._telemetry.update(self._apply_scenario_values(scenario_id, self._scenario_step))
                self._evaluate_alerts()
                await self._emit_event(
                    "telemetry.updated",
                    {
                        "telemetry": self._telemetry,
                        "source": "scenario",
                        "scenario": scenario_id,
                    },
                )

    async def start_scenario(self, scenario_id: str) -> dict[str, Any]:
        async with self._lock:
            if scenario_id not in self._scenario_catalog:
                raise ValueError(f"Unknown scenario: {scenario_id}")
            if self._scenario_task and not self._scenario_task.done():
                self._scenario_task.cancel()
                self._scenario_task = None
            self.mode = "scenario"
            self.active_scenario = scenario_id
            self.scenario_status = "running"
            self.execution_start_time = utc_now_iso()
            self._scenario_step = 0
            self._telemetry = self._apply_scenario_values(scenario_id, self._scenario_step)
            self._baseline = self._baseline_telemetry()
            self._evaluate_alerts()
            await self._emit_event(
                "simulation.started",
                {
                    "scenario": scenario_id,
                    "status": "running",
                    "telemetry": self._telemetry,
                },
            )
            if self._scenario_catalog[scenario_id].get("progressive"):
                self._scenario_task = asyncio.create_task(self._scenario_loop(scenario_id))
            return self.status_snapshot()

    async def pause_scenario(self) -> dict[str, Any]:
        async with self._lock:
            if self.active_scenario is None:
                raise ValueError("No active scenario to pause.")
            if self.scenario_status != "running":
                return self.status_snapshot()
            self.scenario_status = "paused"
            if self._scenario_task and not self._scenario_task.done():
                self._scenario_task.cancel()
                self._scenario_task = None
            await self._emit_event("simulation.paused", {"scenario": self.active_scenario})
            return self.status_snapshot()

    async def resume_scenario(self) -> dict[str, Any]:
        async with self._lock:
            if self.active_scenario is None:
                raise ValueError("No active scenario to resume.")
            if self.scenario_status == "paused":
                self.scenario_status = "running"
                self._scenario_task = asyncio.create_task(self._scenario_loop(self.active_scenario))
                await self._emit_event("simulation.resumed", {"scenario": self.active_scenario})
            return self.status_snapshot()

    async def stop_scenario(self) -> dict[str, Any]:
        async with self._lock:
            self.mode = "manual"
            self.active_scenario = None
            self.scenario_status = "idle"
            if self._scenario_task and not self._scenario_task.done():
                self._scenario_task.cancel()
                self._scenario_task = None
            self.execution_start_time = None
            self._scenario_step = 0
            self._telemetry = self._baseline_telemetry()
            self._evaluate_alerts()
            await self._emit_event("simulation.stopped", {"telemetry": self._telemetry})
            return self.status_snapshot()

    async def patch_telemetry(self, values: TelemetryUpdate) -> dict[str, Any]:
        async with self._lock:
            if self._scenario_task and not self._scenario_task.done():
                self._scenario_task.cancel()
                self._scenario_task = None
                self.active_scenario = None
                self.scenario_status = "idle"
                self.execution_start_time = None
                self.mode = "manual"
            payload = values.model_dump(exclude_none=True)
            self._telemetry.update(payload)
            self._evaluate_alerts()
            await self._emit_event(
                "telemetry.updated",
                {
                    "telemetry": self._telemetry,
                    "source": "manual",
                    "manual_override": True,
                },
            )
            return self.status_snapshot()

    async def reset_simulation(self) -> dict[str, Any]:
        async with self._lock:
            if self._scenario_task and not self._scenario_task.done():
                self._scenario_task.cancel()
                self._scenario_task = None
            self.mode = "manual"
            self.active_scenario = None
            self.scenario_status = "idle"
            self.execution_start_time = None
            self._scenario_step = 0
            self._telemetry = self._baseline_telemetry()
            self._evaluate_alerts()
            await self._emit_event("simulation.reset", {"telemetry": self._telemetry})
            return self.status_snapshot()

    def status_snapshot(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "active_scenario": self.active_scenario,
            "scenario_status": self.scenario_status,
            "execution_start_time": self.execution_start_time,
            "telemetry": self._telemetry,
            "thresholds": self._thresholds(),
        }

    def list_alerts(self) -> list[dict[str, Any]]:
        return [
            {
                **alert,
                "timestamp": alert.get("timestamp", utc_now_iso()),
                "status": alert.get("status", "active"),
            }
            for alert in self.alerts
        ]


simulation_service = SimulationService()
