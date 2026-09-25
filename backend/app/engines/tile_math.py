"""Floor tile order count: area method + waste + remnant threshold, with grid preview."""

from app.engines.helpers import ceil_units, stable_remainder


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
    remnant_threshold_mm: float = 0.0,
    extra_pieces: int = 0,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    base_order: ceil(raw * (1 + waste_pct/100))
    order_count: base_order + extra when the remnant threshold is enabled.

    Remnant strips are room_l mod tile_l (along length) and room_w mod tile_w
    (along width), in mm. A strip that is > 0 and strictly smaller than the
    threshold (mm) triggers the rule; when either direction triggers, a fixed
    extra_pieces is added once. A threshold <= 0 disables the rule and
    order_count equals base_order.
    """
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    base_order = ceil_units(raw * (1 + float(waste_pct) / 100.0))

    rem_l_mm = round(stable_remainder(room_l, tile_l) * 1000.0, 1)
    rem_w_mm = round(stable_remainder(room_w, tile_w) * 1000.0, 1)

    threshold_mm = float(remnant_threshold_mm)
    enabled = threshold_mm > 0
    hit_l = enabled and 0.0 < rem_l_mm < threshold_mm
    hit_w = enabled and 0.0 < rem_w_mm < threshold_mm
    triggered = hit_l or hit_w
    extra_count = int(extra_pieces) if enabled and triggered else 0
    order_count = base_order + extra_count

    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "base_order_count": base_order,
        "order_count": order_count,
        "remnant_enabled": enabled,
        "remnant_threshold_mm": round(threshold_mm, 1) if enabled else 0.0,
        "extra_pieces": int(extra_pieces) if enabled else 0,
        "remnant": {
            "along_length_mm": rem_l_mm,
            "along_width_mm": rem_w_mm,
            "hit_length": bool(hit_l),
            "hit_width": bool(hit_w),
            "extra_count": extra_count,
        },
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
