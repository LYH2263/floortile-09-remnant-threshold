from app.engines.tile_math import layout_preview, tile_count
import pytest


def test_guest_room_600_waste8():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    assert r["area_m2"] == 27.0
    assert r["raw_count"] == 75
    assert r["order_count"] == 81
    assert r["layout"]["cols"] == 10
    assert r["layout"]["rows"] == 8
    assert r["layout"]["grid_count"] == 80


def test_layout_preview_small_room():
    lp = layout_preview(2.5, 2.0, 0.6, 0.6)
    assert lp["cols"] == 5
    assert lp["rows"] == 4
    assert lp["grid_count"] == 20


def test_zero_waste():
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0)
    assert r["raw_count"] == 9
    assert r["order_count"] == 9


def test_remainder_single_edge_triggers():
    # 2.5x2.0 room, 0.6 tile, no waste: raw=14. rem_l=0.1m hits (<0.15), rem_w=0.2m does not.
    r = tile_count(2.5, 2.0, 0.6, 0.6, 0.0, True, 0.15, 2)
    assert r["remainder_l_m"] == 0.1
    assert r["remainder_w_m"] == 0.2
    assert r["remainder_l_triggered"] is True
    assert r["remainder_w_triggered"] is False
    assert r["remainder_trigger_count"] == 1
    assert r["remainder_extra_count"] == 2
    assert r["base_order_count"] == 14
    assert r["order_count"] == 16


def test_remainder_both_edges_trigger():
    r = tile_count(2.5, 2.0, 0.6, 0.6, 0.0, True, 0.25, 2)
    assert r["remainder_trigger_count"] == 2
    assert r["remainder_extra_count"] == 4
    assert r["order_count"] == 18


def test_remainder_equal_threshold_does_not_trigger():
    # rem_l is exactly 0.25m; strict less-than means threshold 0.25 does not trigger.
    r = tile_count(2.25, 2.0, 0.5, 0.5, 0.0, True, 0.25, 2)
    assert r["remainder_l_m"] == 0.25
    assert r["remainder_l_triggered"] is False
    assert r["order_count"] == r["raw_count"] == 18
    # Slightly wider threshold triggers.
    r2 = tile_count(2.25, 2.0, 0.5, 0.5, 0.0, True, 0.251, 2)
    assert r2["remainder_l_triggered"] is True
    assert r2["order_count"] == 20


def test_remainder_exact_fit_no_extra():
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0, True, 0.2, 2)
    assert r["remainder_l_m"] == 0.0
    assert r["remainder_w_m"] == 0.0
    assert r["remainder_trigger_count"] == 0
    assert r["order_count"] == 9


def test_remainder_disabled_keeps_legacy_order():
    r = tile_count(2.5, 2.0, 0.6, 0.6, 0.0)
    assert r["remainder_enabled"] is False
    assert r["order_count"] == r["base_order_count"] == 14
    assert r["remainder_trigger_count"] == 0
    assert r["remainder_extra_count"] == 0


def test_remainder_invalid_threshold_raises():
    with pytest.raises(ValueError):
        tile_count(2.5, 2.0, 0.6, 0.6, 0.0, True, 0.0, 2)
    with pytest.raises(ValueError):
        tile_count(2.5, 2.0, 0.6, 0.6, 0.0, True, 0.1, 0)


def test_remainder_float_edge_exact_division():
    r = tile_count(6.0, 2.0, 0.6, 0.5, 0.0, True, 0.1, 2)
    assert r["remainder_l_m"] == 0.0
    assert r["remainder_w_m"] == 0.0
    assert r["remainder_trigger_count"] == 0
