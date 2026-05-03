import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "bot.db"


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            image_path TEXT,
            source TEXT,
            created_at INTEGER,
            posted INTEGER DEFAULT 0
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS seen_hashes (
            hash TEXT PRIMARY KEY,
            created_at INTEGER
        )"""
    )
    conn.commit()
    conn.close()


async def enqueue_post(text: str, image_path: str | None, source: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO queue (text, image_path, source, created_at) VALUES (?, ?, ?, ?)",
        (text, image_path, source, int(time.time())),
    )
    conn.commit()
    conn.close()


async def get_next_post():
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT id, text, image_path, source FROM queue WHERE posted = 0 ORDER BY created_at LIMIT 1"
    ).fetchone()
    conn.close()
    return row


async def mark_posted(post_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE queue SET posted = 1 WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
