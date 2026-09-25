import json
from datetime import datetime, timezone

from app.db import connect


def insert_run(
    room_id: int,
    tile_id: int,
    waste_pct: float,
    result: dict,
    note: str = "",
    remnant_enabled: bool = False,
    remnant_threshold_mm: float = 0.0,
    extra_pieces: int = 0,
) -> int:
    conn = connect()
    try:
        cur = conn.execute(
            """
            INSERT INTO calc_runs(
                room_id, tile_id, waste_pct, result_json, note, created_at,
                remnant_enabled, remnant_threshold_mm, extra_pieces
            )
            VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (
                room_id,
                tile_id,
                waste_pct,
                json.dumps(result, ensure_ascii=False),
                note,
                datetime.now(timezone.utc).isoformat(),
                1 if remnant_enabled else 0,
                float(remnant_threshold_mm),
                int(extra_pieces),
            ),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def list_runs(limit: int = 50):
    conn = connect()
    try:
        rows = conn.execute(
            """
            SELECT r.*, rm.name AS room_name, t.name AS tile_name
            FROM calc_runs r
            LEFT JOIN rooms rm ON rm.id = r.room_id
            LEFT JOIN tiles t ON t.id = r.tile_id
            ORDER BY r.id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        out = []
        for row in rows:
            d = dict(row)
            d["result"] = json.loads(d.pop("result_json"))
            out.append(d)
        return out
    finally:
        conn.close()


def get_run(run_id: int):
    conn = connect()
    try:
        row = conn.execute(
            """
            SELECT r.*, rm.name AS room_name, t.name AS tile_name
            FROM calc_runs r
            LEFT JOIN rooms rm ON rm.id = r.room_id
            LEFT JOIN tiles t ON t.id = r.tile_id
            WHERE r.id=?
            """,
            (run_id,),
        ).fetchone()
        if not row:
            return None
        d = dict(row)
        d["result"] = json.loads(d.pop("result_json"))
        return d
    finally:
        conn.close()
