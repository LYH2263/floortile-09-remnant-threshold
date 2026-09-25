"""Floor tile order count: area method + optional grid layout preview."""

import math

from app.engines.helpers import ceil_units


def _remainder_strip(room_dim: float, tile_dim: float) -> float:
    """Leftover strip (metres) after tiling one edge: room_dim mod tile_dim.

    Returns 0.0 for an exact fit, using the same 1e-9 tolerance as ceil_units
    so floating-point tails (e.g. 6.0 % 0.6) are not mistaken for offcuts.
    """
    rem = math.fmod(float(room_dim), float(tile_dim))
    if rem <= 1e-9 or rem >= float(tile_dim) - 1e-9:
        return 0.0
    return rem


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
    remainder_enabled: bool = False,
    remainder_threshold_m: float = 0.0,
    remainder_extra_per_strip: int = 0,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    base_order_count: ceil(raw * (1 + waste_pct/100))
    order_count: base_order_count plus fixed extra pieces for each edge whose
                 leftover strip is >0 and strictly below the threshold.
    """
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    if remainder_enabled and (
        remainder_threshold_m <= 0 or remainder_extra_per_strip < 1
    ):
        raise ValueError("remainder threshold must be > 0 and extra pieces >= 1")

    raw = ceil_units(area / piece)
    base_order = ceil_units(raw * (1 + float(waste_pct) / 100.0))

    rem_l = _remainder_strip(room_l, tile_l)
    rem_w = _remainder_strip(room_w, tile_w)
    threshold = float(remainder_threshold_m)
    l_hit = bool(remainder_enabled) and 0.0 < rem_l < threshold
    w_hit = bool(remainder_enabled) and 0.0 < rem_w < threshold
    trigger_count = int(l_hit) + int(w_hit)
    extra_count = trigger_count * int(remainder_extra_per_strip)

    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "base_order_count": base_order,
        "order_count": base_order + extra_count,
        "remainder_enabled": bool(remainder_enabled),
        "remainder_l_m": round(rem_l, 4),
        "remainder_w_m": round(rem_w, 4),
        "remainder_threshold_m": round(threshold, 3),
        "remainder_extra_per_strip": int(remainder_extra_per_strip),
        "remainder_l_triggered": l_hit,
        "remainder_w_triggered": w_hit,
        "remainder_trigger_count": trigger_count,
        "remainder_extra_count": extra_count,
        "layout": layout,
    }


def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    """Grid count if tiles are laid on a full rectangular lattice (may exceed area method)."""
    cols = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    grid_count = cols * rows
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": grid_count,
    }
