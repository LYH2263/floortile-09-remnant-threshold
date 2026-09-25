from app.engines.tile_math import tile_count


def test_disabled_threshold_matches_legacy_order():
    # threshold <= 0 (or omitted): order equals the pre-change waste value.
    r = tile_count(8.0, 1.2, 0.8, 0.8, 8.0, 0.0, 2)
    assert r["raw_count"] == 15
    assert r["base_order_count"] == 17
    assert r["order_count"] == 17
    assert r["remnant_enabled"] is False
    assert r["remnant"]["extra_count"] == 0


def test_default_signature_unchanged():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    assert r["order_count"] == 81
    assert r["remnant_enabled"] is False


def test_remnant_below_threshold_triggers_once():
    # corridor: width strip 1.2 mod 0.8 = 400 mm; length is seam (0 mm).
    r = tile_count(8.0, 1.2, 0.8, 0.8, 8.0, 500.0, 2)
    assert r["remnant"]["along_width_mm"] == 400.0
    assert r["remnant"]["along_length_mm"] == 0.0
    assert r["remnant"]["hit_width"] is True
    assert r["remnant"]["hit_length"] is False
    assert r["remnant"]["extra_count"] == 2
    assert r["base_order_count"] == 17
    assert r["order_count"] == 19


def test_remnant_above_threshold_no_extra():
    r = tile_count(8.0, 1.2, 0.8, 0.8, 8.0, 300.0, 2)
    assert r["remnant"]["hit_width"] is False
    assert r["order_count"] == 17


def test_remnant_equal_to_threshold_does_not_trigger():
    # 2.5 mod 0.6 = 100 mm; strictly smaller than threshold required.
    r = tile_count(2.5, 2.0, 0.6, 0.6, 0.0, 100.0, 3)
    assert r["remnant"]["along_length_mm"] == 100.0
    assert r["remnant"]["hit_length"] is False
    assert r["order_count"] == r["base_order_count"]


def test_either_direction_triggers_fixed_pieces_only_once():
    # along length 100 mm (<150), along width 200 mm: fixed add happens once.
    r = tile_count(2.5, 2.0, 0.6, 0.6, 0.0, 150.0, 3)
    assert r["remnant"]["hit_length"] is True
    assert r["remnant"]["hit_width"] is False
    assert r["remnant"]["extra_count"] == 3
    assert r["raw_count"] == 14
    assert r["order_count"] == 17


def test_seam_length_never_triggers_and_wide_strip_below_order_unchanged():
    # length 6.0 is a 0.6 seam (0 mm); width 4.5 leaves a 300 mm strip that is
    # not smaller than a 50 mm threshold, so no add and order stays at 81.
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, 50.0, 5)
    assert r["remnant"]["along_length_mm"] == 0.0
    assert r["remnant"]["along_width_mm"] == 300.0
    assert r["remnant"]["hit_length"] is False
    assert r["remnant"]["hit_width"] is False
    assert r["order_count"] == 81
