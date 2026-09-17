"""
Task handler for the SQL generation task.
Prompts the model to generate a SQL query from a natural language question,
then validates it by executing both the expected and predicted queries
against a persistent test database and comparing the result sets.
"""

from app.tasks.test_db import get_test_connection

# ------------------------------------------------------------------
# The database schema – must exactly match the schema used to build
# the persistent test database (scripts/build_test_db.py).
# ------------------------------------------------------------------
DB_SCHEMA = """
CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL,
    building TEXT,
    budget REAL,
    dean_id INTEGER
);

CREATE TABLE professors (
    prof_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    dept_id INTEGER,
    hire_date DATE,
    salary REAL,
    is_tenured BOOLEAN,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    major_dept_id INTEGER,
    year_of_study INTEGER CHECK (year_of_study BETWEEN 1 AND 6),
    gpa REAL CHECK (gpa BETWEEN 0.0 AND 4.0),
    graduation_date DATE,
    FOREIGN KEY (major_dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_code TEXT UNIQUE,
    title TEXT,
    credits INTEGER,
    dept_id INTEGER,
    max_enrollment INTEGER,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE offerings (
    offering_id INTEGER PRIMARY KEY,
    course_id INTEGER,
    prof_id INTEGER,
    semester TEXT CHECK (semester IN ('Fall', 'Spring', 'Summer')),
    year INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (prof_id) REFERENCES professors(prof_id)
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    offering_id INTEGER,
    student_id INTEGER,
    grade TEXT CHECK (grade IN ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'F', 'W')),
    enrollment_date DATE,
    FOREIGN KEY (offering_id) REFERENCES offerings(offering_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
"""


# ------------------------------------------------------------------
# Prompt Builder
# ------------------------------------------------------------------
def build_prompt(case: dict) -> tuple[str, str]:
    """
    Build the system and user prompts for SQL generation.
    Returns (system_prompt, user_prompt).
    """
    system_prompt = """You are a SQL expert. Convert the following natural language question into a valid SQL query.

IMPORTANT RULES:
- Output ONLY the raw SQL query.
- Do NOT include any explanation, markdown, backticks, or JSON.
- Do NOT wrap the query in any structure.
- The query must be a single string.
- End your query with a semicolon.

Example:
Question: List all students.
SQL Query: SELECT * FROM students;
"""

    user_prompt = f"""Database Schema:
{DB_SCHEMA}

Convert the following question into a raw SQL query.
Output ONLY the query string. No JSON, no markdown, no extra text.

Question: {case['question']}

SQL Query:"""

    return system_prompt, user_prompt


# ------------------------------------------------------------------
# Scoring Function (Executes both queries and compares results)
# ------------------------------------------------------------------
def score(raw: dict, case: dict) -> dict:
    """
    Score the SQL result by executing both the expected and predicted SQL
    on the persistent test database and comparing the result sets.

    Two queries are considered equivalent iff they return the exact same
    set of rows (sorted) when executed on the test database.
    """
    expected = case.get("sql", "").strip()
    predicted = raw.get("response", "").strip()

    # Normalize SQL: strip markdown code fences and trailing semicolon
    def normalize(sql: str) -> str:
        sql = sql.strip()
        if sql.startswith("```sql"):
            sql = sql[6:]
        elif sql.startswith("```"):
            sql = sql[3:]
        sql = sql.strip()
        if sql.endswith("```"):
            sql = sql[:-3]
        return sql.strip().rstrip(";").strip()

    expected_norm = normalize(expected)
    predicted_norm = normalize(predicted)

    # If either SQL is empty, it's an automatic failure
    if not expected_norm or not predicted_norm:
        return {
            "score": 0.0,
            "is_correct": False,
            "expected_sql": expected_norm,
            "predicted_sql": predicted_norm,
            "error": "Empty SQL statement",
        }

    conn = get_test_connection()
    cursor = conn.cursor()

    try:
        # Execute both queries and fetch all rows
        expected_rows = cursor.execute(expected_norm).fetchall()
        predicted_rows = cursor.execute(predicted_norm).fetchall()

        # Sort rows to avoid false failures due to arbitrary row order
        # (tuples are comparable element‑wise)
        is_correct = sorted(expected_rows) == sorted(predicted_rows)

        return {
            "score": 1.0 if is_correct else 0.0,
            "is_correct": is_correct,
            "expected_sql": expected_norm,
            "predicted_sql": predicted_norm,
            "error": None,
        }

    except Exception as e:
        # Query execution failed – treat as incorrect
        return {
            "score": 0.0,
            "is_correct": False,
            "expected_sql": expected_norm,
            "predicted_sql": predicted_norm,
            "error": str(e),
        }

    finally:
        conn.close()