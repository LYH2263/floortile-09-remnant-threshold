from pydantic import BaseModel, Field


class SettingsUpdate(BaseModel):
    remainder_threshold_mm: int = Field(gt=0)
    remainder_extra_pieces: int = Field(ge=1)
