from pydantic import BaseModel


class EstimateRequest(BaseModel):
    room_id: int
    tile_id: int
    waste_pct: float | None = None
    remainder_enabled: bool = False
    remainder_threshold_mm: float | None = None
    remainder_extra_pieces: int | None = None
    save: bool = False
    note: str = ""


class EstimateResponse(BaseModel):
    room_id: int
    tile_id: int
    area_m2: float
    piece_m2: float
    raw_count: int
    waste_pct: float
    base_order_count: int
    order_count: int
    remainder_enabled: bool
    remainder_l_m: float
    remainder_w_m: float
    remainder_threshold_m: float
    remainder_extra_per_strip: int
    remainder_l_triggered: bool
    remainder_w_triggered: bool
    remainder_trigger_count: int
    remainder_extra_count: int
    layout: dict
    run_id: int | None = None
