"""SQLite storage for tickets."""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    text TEXT NOT NULL,
    category TEXT NOT NULL,
    assignee TEXT,
    status TEXT NOT NULL DEFAULT 'open'
)
"""


def connect(path: str = "tickets.db") -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute(SCHEMA)
    return connection


def add(connection, sender: str, text: str, category: str) -> int:
    cursor = connection.execute(
        "INSERT INTO tickets (sender, text, category) VALUES (?, ?, ?)", (sender, text, category)
    )
    connection.commit()
    return cursor.lastrowid


def list_open(connection, category: str | None = None) -> list[sqlite3.Row]:
    if category:
        return connection.execute(
            "SELECT * FROM tickets WHERE status = 'open' AND category = ? ORDER BY id", (category,)
        ).fetchall()
    return connection.execute("SELECT * FROM tickets WHERE status = 'open' ORDER BY id").fetchall()


def close(connection, ticket_id: int) -> None:
    connection.execute("UPDATE tickets SET status = 'closed' WHERE id = ?", (ticket_id,))
    connection.commit()
