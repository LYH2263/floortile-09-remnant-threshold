from app.config import (
    DEFAULT_REMAINDER_EXTRA_PIECES,
    DEFAULT_REMAINDER_THRESHOLD_MM,
    DEFAULT_WASTE_PCT,
)
from app.db import connect

_DEFAULTS = {
    "waste_pct": str(DEFAULT_WASTE_PCT),
    "remainder_threshold_mm": str(DEFAULT_REMAINDER_THRESHOLD_MM),
    "remainder_extra_pieces": str(DEFAULT_REMAINDER_EXTRA_PIECES),
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


def get_remainder_threshold_mm() -> int:
    return int(float(get_all()["remainder_threshold_mm"]))


def get_remainder_extra_pieces() -> int:
    return int(float(get_all()["remainder_extra_pieces"]))


def upsert(key: str, value: str) -> None:
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO settings(key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )
        conn.commit()
    finally:
        conn.close()
