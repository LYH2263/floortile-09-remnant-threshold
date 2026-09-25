from fastapi import HTTPException

from app.engines.tile_math import tile_count
from app.repositories import history, rooms, settings_repo, tiles


def run_estimate(
    room_id: int,
    tile_id: int,
    waste_pct: float | None,
    save: bool,
    note: str,
    remainder_enabled: bool = False,
    remainder_threshold_mm: float | None = None,
    remainder_extra_pieces: int | None = None,
):
    room = rooms.get_room(room_id)
    if not room:
        raise HTTPException(404, "room not found")
    tile = tiles.get_tile(tile_id)
    if not tile:
        raise HTTPException(404, "tile not found")
    if room.get("data_quality") == "dirty":
        raise HTTPException(422, "room marked dirty; fix dimensions before estimate")

    waste = float(waste_pct) if waste_pct is not None else settings_repo.get_waste_pct()
    threshold_mm = (
        float(remainder_threshold_mm)
        if remainder_threshold_mm is not None
        else float(settings_repo.get_remainder_threshold_mm())
    )
    extra_pieces = (
        int(remainder_extra_pieces)
        if remainder_extra_pieces is not None
        else settings_repo.get_remainder_extra_pieces()
    )

    if remainder_enabled and threshold_mm <= 0:
        raise HTTPException(422, "remainder threshold must be > 0 when enabled")
    if remainder_enabled and extra_pieces < 1:
        raise HTTPException(422, "remainder extra pieces must be >= 1 when enabled")

    calc = tile_count(
        room["length"],
        room["width"],
        tile["tile_l"],
        tile["tile_w"],
        waste,
        remainder_enabled=remainder_enabled,
        remainder_threshold_m=threshold_mm / 1000.0,
        remainder_extra_per_strip=extra_pieces,
    )

    run_id = None
    if save:
        payload = {**calc, "room_id": room_id, "tile_id": tile_id, "tile": dict(tile)}
        run_id = history.insert_run(room_id, tile_id, waste, payload, note)

    return {
        "room_id": room_id,
        "tile_id": tile_id,
        "room": room,
        "tile": tile,
        "run_id": run_id,
        **calc,
    }
