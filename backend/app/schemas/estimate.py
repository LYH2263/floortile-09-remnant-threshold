from pydantic import BaseModel


class EstimateRequest(BaseModel):
    room_id: int
    tile_id: int
    waste_pct: float | None = None
    save: bool = False
    note: str = ""
    remnant_enabled: bool = False
    remnant_threshold_mm: float | None = None
    extra_pieces: int | None = None


class EstimateResponse(BaseModel):
    room_id: int
    tile_id: int
    room_name: str
    tile_name: str
    area_m2: float
    piece_m2: float
    raw_count: int
    waste_pct: float
    base_order_count: int
    order_count: int
    remnant_enabled: bool
    remnant_threshold_mm: float
    extra_pieces: int
    remnant: dict
    layout: dict
    run_id: int | None = None


class SettingsUpdateRequest(BaseModel):
    waste_pct: float | None = None
    remnant_threshold_mm: float | None = None
    extra_pieces: int | None = None
