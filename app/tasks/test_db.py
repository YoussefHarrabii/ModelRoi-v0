import sqlite3
from pathlib import Path

# Path to the test database
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "test_data.db"

def _ensure_db_exists():
    """Build the test database on first use (it's gitignored, so CI/fresh clones lack it)."""
    if DB_PATH.exists():
        return
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    from app.tasks.build_sql_database import SCHEMA, populate_database

    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.executescript(SCHEMA)
        populate_database(conn)
    finally:
        conn.close()


def get_test_connection():
    """
    Return a read-only connection to the persistent test database,
    building it automatically on first use.
    """
    _ensure_db_exists()
    # Use URI mode with `mode=ro` for true read‑only access
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)

# Optional: quick sanity check
if __name__ == "__main__":
    try:
        conn = get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM departments")
        print(f"Departments count: {cursor.fetchone()[0]}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")