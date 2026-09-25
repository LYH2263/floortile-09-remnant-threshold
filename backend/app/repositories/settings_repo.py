from app.config import (
    DEFAULT_EXTRA_PIECES,
    DEFAULT_REMNANT_THRESHOLD_MM,
    DEFAULT_WASTE_PCT,
)
from app.db import connect

_DEFAULTS = {
    "waste_pct": str(DEFAULT_WASTE_PCT),
    "remnant_threshold_mm": str(DEFAULT_REMNANT_THRESHOLD_MM),
    "extra_pieces": str(DEFAULT_EXTRA_PIECES),
}


def get_all() -> dict:
    conn = connect()
    try:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        out = {r["key"]: r["value"] for r in rows}
        for key, default in _DEFAULTS.items():
            if key not in out:
                out[key] = default
        return out
    finally:
        conn.close()


def get_waste_pct() -> float:
    return float(get_all().get("waste_pct", str(DEFAULT_WASTE_PCT)))


def get_remnant_threshold_mm() -> float:
    return float(get_all().get("remnant_threshold_mm", str(DEFAULT_REMNANT_THRESHOLD_MM)))


def get_extra_pieces() -> int:
    return int(float(get_all().get("extra_pieces", str(DEFAULT_EXTRA_PIECES))))


def update_settings(
    waste_pct: float | None = None,
    remnant_threshold_mm: float | None = None,
    extra_pieces: int | None = None,
) -> dict:
    if waste_pct is not None and float(waste_pct) < 0:
        raise ValueError("waste_pct must be >= 0")
    if remnant_threshold_mm is not None and float(remnant_threshold_mm) <= 0:
        raise ValueError("remnant_threshold_mm must be > 0")
    if extra_pieces is not None and int(extra_pieces) < 0:
        raise ValueError("extra_pieces must be >= 0")

    values = {}
    if waste_pct is not None:
        values["waste_pct"] = str(float(waste_pct))
    if remnant_threshold_mm is not None:
        values["remnant_threshold_mm"] = str(float(remnant_threshold_mm))
    if extra_pieces is not None:
        values["extra_pieces"] = str(int(extra_pieces))

    if not values:
        return get_all()

    conn = connect()
    try:
        conn.executemany(
            "INSERT INTO settings(key,value) VALUES(?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            list(values.items()),
        )
        conn.commit()
    finally:
        conn.close()
    return get_all()
