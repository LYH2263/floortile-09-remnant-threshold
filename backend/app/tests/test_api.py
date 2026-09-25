import os
import tempfile

os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="floortile-test-")

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def _client():
    return TestClient(app).__enter__()


client = _client()


def test_legacy_preview_unchanged():
    r = client.get("/api/estimate", params={"room_id": 1, "tile_id": 1})
    assert r.status_code == 200
    body = r.json()
    assert body["order_count"] == 81
    assert body["base_order_count"] == 81
    assert body["remainder_enabled"] is False
    assert body["remainder_extra_count"] == 0


def test_zero_threshold_fails_and_does_not_write_history():
    before = client.get("/api/runs").json()["items"]
    r = client.get(
        "/api/estimate",
        params={
            "room_id": 1,
            "tile_id": 1,
            "remainder_enabled": "true",
            "remainder_threshold_mm": 0,
        },
    )
    assert r.status_code == 422
    r2 = client.post(
        "/api/estimate",
        json={
            "room_id": 1,
            "tile_id": 1,
            "save": True,
            "remainder_enabled": True,
            "remainder_threshold_mm": -5,
        },
    )
    assert r2.status_code == 422
    after = client.get("/api/runs").json()["items"]
    assert len(after) == len(before)


def test_settings_validation_and_update():
    bad = client.post(
        "/api/settings",
        json={"remainder_threshold_mm": 0, "remainder_extra_pieces": 2},
    )
    assert bad.status_code == 422
    ok = client.post(
        "/api/settings",
        json={"remainder_threshold_mm": 120, "remainder_extra_pieces": 3},
    )
    assert ok.status_code == 200
    assert ok.json()["remainder_threshold_mm"] == "120"
    assert ok.json()["remainder_extra_pieces"] == "3"
    # Defaults apply to new estimates.
    r = client.get(
        "/api/estimate",
        params={"room_id": 1, "tile_id": 1, "remainder_enabled": "true"},
    )
    assert r.json()["remainder_threshold_m"] == 0.12
    assert r.json()["remainder_extra_per_strip"] == 3


def test_saved_run_pins_snapshot_fields():
    r = client.post(
        "/api/estimate",
        json={
            "room_id": 1,
            "tile_id": 1,
            "save": True,
            "note": "门槛单",
            "remainder_enabled": True,
            "remainder_threshold_mm": 50,
            "remainder_extra_pieces": 4,
        },
    )
    assert r.status_code == 200
    run_id = r.json()["run_id"]
    snap = client.get(f"/api/runs/{run_id}").json()["result"]
    preview = r.json()
    for key in (
        "base_order_count",
        "order_count",
        "remainder_l_m",
        "remainder_w_m",
        "remainder_threshold_m",
        "remainder_extra_per_strip",
        "remainder_trigger_count",
        "remainder_extra_count",
        "remainder_enabled",
    ):
        assert snap[key] == preview[key]
    assert snap["order_count"] == snap["base_order_count"] + snap["remainder_extra_count"]

    # Changing the default must not alter the pinned historical snapshot.
    client.post(
        "/api/settings",
        json={"remainder_threshold_mm": 300, "remainder_extra_pieces": 9},
    )
    snap_after = client.get(f"/api/runs/{run_id}").json()["result"]
    assert snap_after["remainder_threshold_m"] == 0.05
    assert snap_after["order_count"] == snap["order_count"]
