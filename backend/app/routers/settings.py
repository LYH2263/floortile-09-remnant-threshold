from fastapi import APIRouter, HTTPException

from app.repositories import settings_repo
from app.schemas.estimate import SettingsUpdateRequest

router = APIRouter(tags=["settings"])


@router.get("/settings")
def get_settings():
    return settings_repo.get_all()


@router.put("/settings")
def update_settings(body: SettingsUpdateRequest):
    try:
        return settings_repo.update_settings(
            body.waste_pct, body.remnant_threshold_mm, body.extra_pieces
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc))
