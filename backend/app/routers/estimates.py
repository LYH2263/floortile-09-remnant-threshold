from fastapi import APIRouter, Query

from app.schemas.estimate import EstimateRequest
from app.services import estimate_service

router = APIRouter(tags=["estimates"])


@router.get("/estimate")
def estimate_get(
    room_id: int = Query(...),
    tile_id: int = Query(...),
    waste_pct: float | None = None,
    save: bool = False,
    remnant_enabled: bool = False,
    remnant_threshold_mm: float | None = None,
    extra_pieces: int | None = None,
):
    return estimate_service.run_estimate(
        room_id,
        tile_id,
        waste_pct,
        save,
        "",
        remnant_enabled,
        remnant_threshold_mm,
        extra_pieces,
    )


@router.post("/estimate")
def estimate_post(body: EstimateRequest):
    return estimate_service.run_estimate(
        body.room_id,
        body.tile_id,
        body.waste_pct,
        body.save,
        body.note,
        body.remnant_enabled,
        body.remnant_threshold_mm,
        body.extra_pieces,
    )
