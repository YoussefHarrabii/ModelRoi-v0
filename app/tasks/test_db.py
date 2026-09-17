import sqlite3
from pathlib import Path

# Path to the test database
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "test_data.db"

def get_test_connection():
    """
    Return a read‑only connection to the persistent test database.
    Raises FileNotFoundError if the database has not been built yet.
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Test database not found at {DB_PATH}. "
            "Please run `python scripts/build_test_db.py` first."
        )
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