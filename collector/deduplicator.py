import sqlite3
import hashlib
from publisher.queue_manager import DB_PATH


def get_hash(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def is_duplicate(text: str) -> bool:
    h = get_hash(text)
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT 1 FROM seen_hashes WHERE hash = ?", (h,)).fetchone()
    conn.close()
    return bool(row)


def mark_seen(text: str) -> None:
    h = get_hash(text)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR IGNORE INTO seen_hashes (hash, created_at) VALUES (?, strftime('%s','now'))", (h,))
    conn.commit()
    conn.close()
