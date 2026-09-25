from fastapi import APIRouter, Query

from app.schemas.estimate import EstimateRequest
from app.services import estimate_service

router = APIRouter(tags=["estimates"])


@router.get("/estimate")
def estimate_get(
    room_id: int = Query(...),
    tile_id: int = Query(...),
    waste_pct: float | None = None,
    remainder_enabled: bool = False,
    remainder_threshold_mm: float | None = None,
    remainder_extra_pieces: int | None = None,
    save: bool = False,
):
    return estimate_service.run_estimate(
        room_id,
        tile_id,
        waste_pct,
        save,
        "",
        remainder_enabled,
        remainder_threshold_mm,
        remainder_extra_pieces,
    )


@router.post("/estimate")
def estimate_post(body: EstimateRequest):
    return estimate_service.run_estimate(
        body.room_id,
        body.tile_id,
        body.waste_pct,
        body.save,
        body.note,
        body.remainder_enabled,
        body.remainder_threshold_mm,
        body.remainder_extra_pieces,
    )
