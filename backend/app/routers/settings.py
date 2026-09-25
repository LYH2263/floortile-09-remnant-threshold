from fastapi import APIRouter

from app.repositories import settings_repo
from app.schemas.settings import SettingsUpdate

router = APIRouter(tags=["settings"])


@router.get("/settings")
def get_settings():
    return settings_repo.get_all()


@router.post("/settings")
def update_settings(body: SettingsUpdate):
    settings_repo.upsert("remainder_threshold_mm", str(body.remainder_threshold_mm))
    settings_repo.upsert("remainder_extra_pieces", str(body.remainder_extra_pieces))
    return settings_repo.get_all()
