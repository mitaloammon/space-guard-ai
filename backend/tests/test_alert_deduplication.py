import time

from app.core.simulation import SimulationService


def _active_alerts(service: SimulationService, alert_type: str | None = None):
    return [
        alert
        for alert in service.list_alerts()
        if alert.get("status") == "active"
        and (alert_type is None or alert.get("alert_type") == alert_type)
    ]


def test_repeated_high_temperature_updates_stay_single_active_alert():
    service = SimulationService()

    service._telemetry["temperature_celsius"] = 40.0
    service._evaluate_alerts()
    first_pass = _active_alerts(service, "high_temperature")
    assert len(first_pass) == 1
    assert first_pass[0]["alert_type"] == "high_temperature"

    service._telemetry["temperature_celsius"] = 40.0
    service._evaluate_alerts()
    second_pass = _active_alerts(service, "high_temperature")

    assert len(second_pass) == 1
    assert second_pass[0]["id"] == first_pass[0]["id"]
    assert second_pass[0]["severity"] == "critical"


def test_existing_high_temperature_alert_updates_in_place():
    service = SimulationService()
    service._telemetry["temperature_celsius"] = 40.0
    service._evaluate_alerts()

    first_alert = _active_alerts(service, "high_temperature")[0]
    first_timestamp = first_alert["timestamp"]

    service._telemetry["temperature_celsius"] = 42.5
    service._evaluate_alerts()

    updated_alert = _active_alerts(service, "high_temperature")[0]
    assert len(_active_alerts(service, "high_temperature")) == 1
    assert updated_alert["id"] == first_alert["id"]
    assert updated_alert["timestamp"] == first_timestamp
    assert updated_alert["severity"] == "critical"
    assert updated_alert["status"] == "active"
    assert "updated_at" in updated_alert


def test_high_temperature_alert_resolves_when_it_clears_and_reappears_later():
    service = SimulationService()

    service._telemetry["temperature_celsius"] = 40.0
    service._evaluate_alerts()
    assert len(_active_alerts(service, "high_temperature")) == 1

    service._telemetry["temperature_celsius"] = 28.0
    service._evaluate_alerts()
    resolved_alerts = [alert for alert in service.list_alerts() if alert.get("alert_type") == "high_temperature"]
    assert len(resolved_alerts) == 1
    assert resolved_alerts[0]["status"] == "resolved"

    time.sleep(0.01)
    service._telemetry["temperature_celsius"] = 39.5
    service._evaluate_alerts()
    renewed_alerts = _active_alerts(service, "high_temperature")
    assert len(renewed_alerts) == 1
    assert renewed_alerts[0]["status"] == "active"
    assert renewed_alerts[0]["id"] == resolved_alerts[0]["id"]
    assert renewed_alerts[0]["timestamp"] >= resolved_alerts[0]["timestamp"]


def test_different_alert_conditions_remain_independent():
    service = SimulationService()
    service._telemetry.update({
        "temperature_celsius": 41.0,
        "battery_level": 10.0,
        "radiation_rate_msv_h": 1.8,
    })
    service._evaluate_alerts()

    active_types = {alert["alert_type"] for alert in service.list_alerts() if alert.get("status") == "active"}
    assert {"high_temperature", "low_battery", "radiation_increase"}.issubset(active_types)
    assert len(_active_alerts(service)) == 3


def test_repeated_telemetry_cycles_do_not_duplicate_websocket_alert_payloads():
    service = SimulationService()

    service._telemetry["temperature_celsius"] = 38.0
    service._evaluate_alerts()
    first_snapshot = service.list_alerts()

    service._telemetry["temperature_celsius"] = 38.0
    service._evaluate_alerts()
    second_snapshot = service.list_alerts()

    active_high_temp = [alert for alert in second_snapshot if alert.get("alert_type") == "high_temperature" and alert.get("status") == "active"]
    assert len(active_high_temp) == 1
    assert len(first_snapshot) == len(second_snapshot)
    assert len([alert for alert in second_snapshot if alert.get("status") == "active"]) == 1
