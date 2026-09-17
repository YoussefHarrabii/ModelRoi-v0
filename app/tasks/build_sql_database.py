#!/usr/bin/env python3
"""
Build a large, persistent test database for SQL evaluation.
Run this script once to generate `data/test_data.db`.
"""

import os
import sys
import sqlite3
import random
import string
from datetime import datetime, timedelta

# -------- Data Generators --------
random.seed(42)  # deterministic for reproducibility

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_name():
    return random_string(6).capitalize()

def random_choice(lst):
    return random.choice(lst)

# -------- Constants --------
DEPARTMENT_NAMES = [
    "Computer Science", "Mathematics", "Physics", "Chemistry", "Biology",
    "Engineering", "Economics", "Psychology", "Philosophy", "History",
    "Political Science", "Sociology", "Linguistics", "Art", "Music"
]
BUILDINGS = ["Main", "Science", "Engineering", "Arts", "Library", "East", "West"]
SEMESTERS = ["Fall", "Spring", "Summer"]
GRADES = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'F', 'W']

# -------- Schema --------
SCHEMA = """
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

# -------- Populate Database --------
def populate_database(conn):
    cursor = conn.cursor()

    # 1. Departments
    dept_ids = []
    for i, name in enumerate(DEPARTMENT_NAMES, start=1):
        dept_id = i
        dept_ids.append(dept_id)
        building = random_choice(BUILDINGS)
        budget = round(random.uniform(200000, 2000000), 2)
        cursor.execute(
            "INSERT INTO departments (dept_id, dept_name, building, budget, dean_id) VALUES (?, ?, ?, ?, ?)",
            (dept_id, name, building, budget, None)
        )

    # 2. Professors (200)
    prof_ids = []
    for i in range(1, 201):
        prof_id = i
        prof_ids.append(prof_id)
        first = random_name()
        last = random_name()
        dept_id = random_choice(dept_ids)
        hire_date = random_date(datetime(1990, 1, 1), datetime(2023, 12, 31))
        salary = round(random.uniform(60000, 180000), 2)
        is_tenured = random_choice([0, 1])
        cursor.execute(
            "INSERT INTO professors (prof_id, first_name, last_name, dept_id, hire_date, salary, is_tenured) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (prof_id, first, last, dept_id, hire_date, salary, is_tenured)
        )

    # Assign deans (some departments have a dean)
    for dept_id in dept_ids:
        cursor.execute("SELECT prof_id FROM professors WHERE dept_id = ?", (dept_id,))
        profs = [row[0] for row in cursor.fetchall()]
        if profs and random.random() < 0.7:
            dean = random_choice(profs)
            cursor.execute("UPDATE departments SET dean_id = ? WHERE dept_id = ?", (dean, dept_id))

    # 3. Students (1000)
    student_ids = []
    for i in range(1, 1001):
        student_id = i
        student_ids.append(student_id)
        first = random_name()
        last = random_name()
        major = random_choice(dept_ids)
        year = random.randint(1, 6)
        gpa = round(random.uniform(0.0, 4.0), 2)
        grad_date = random_date(datetime(2020, 1, 1), datetime(2028, 12, 31)) if random.random() < 0.6 else None
        cursor.execute(
            "INSERT INTO students (student_id, first_name, last_name, major_dept_id, year_of_study, gpa, graduation_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (student_id, first, last, major, year, gpa, grad_date)
        )

    # 4. Courses (100)
    course_ids = []
    for i in range(1, 101):
        course_id = i
        course_ids.append(course_id)
        dept_id = random_choice(dept_ids)
        # Generate unique course code
        prefix = DEPARTMENT_NAMES[dept_id-1][:3].upper()
        course_code = f"{prefix}{random.randint(100, 499)}"
        cursor.execute("SELECT 1 FROM courses WHERE course_code = ?", (course_code,))
        while cursor.fetchone():
            course_code = f"{prefix}{random.randint(100, 499)}"
            cursor.execute("SELECT 1 FROM courses WHERE course_code = ?", (course_code,))
        title = f"{random_string(4)} {random_string(6)}"
        credits = random_choice([1, 2, 3, 4])
        max_enrollment = random.randint(20, 60)
        cursor.execute(
            "INSERT INTO courses (course_id, course_code, title, credits, dept_id, max_enrollment) VALUES (?, ?, ?, ?, ?, ?)",
            (course_id, course_code, title, credits, dept_id, max_enrollment)
        )

    # 5. Offerings (500)
    offering_ids = []
    for i in range(1, 501):
        offering_id = i
        offering_ids.append(offering_id)
        course_id = random_choice(course_ids)
        prof_id = random_choice(prof_ids)
        semester = random_choice(SEMESTERS)
        year = random.randint(2018, 2025)
        cursor.execute(
            "INSERT INTO offerings (offering_id, course_id, prof_id, semester, year) VALUES (?, ?, ?, ?, ?)",
            (offering_id, course_id, prof_id, semester, year)
        )

    # 6. Enrollments (5000)
    for i in range(1, 5001):
        enrollment_id = i
        offering_id = random_choice(offering_ids)
        student_id = random_choice(student_ids)
        grade = random_choice(GRADES)
        enrollment_date = random_date(datetime(2018, 1, 1), datetime(2025, 6, 30))
        cursor.execute(
            "INSERT INTO enrollments (enrollment_id, offering_id, student_id, grade, enrollment_date) VALUES (?, ?, ?, ?, ?)",
            (enrollment_id, offering_id, student_id, grade, enrollment_date)
        )

    # -------- ADD EDGE CASES --------
    # 1. Student with NULL major_dept_id
    cursor.execute("""
        INSERT INTO students (student_id, first_name, last_name, major_dept_id, year_of_study, gpa, graduation_date)
        VALUES (9999, 'Null', 'Major', NULL, 1, 0.0, NULL)
    """)

    # 2. Ensure a department in 'West Hall' exists
    cursor.execute("SELECT dept_id FROM departments WHERE building = 'West' LIMIT 1")
    row = cursor.fetchone()
    if not row:
        # If no department is in 'West', update one
        cursor.execute("UPDATE departments SET building = 'West' WHERE dept_id = 1")
        cursor.execute("SELECT dept_id FROM departments WHERE building = 'West' LIMIT 1")
        row = cursor.fetchone()
    dept_id = row[0]

    # Insert a course in that department with max_enrollment > 50
    cursor.execute("""
        INSERT INTO courses (course_id, course_code, title, credits, dept_id, max_enrollment)
        VALUES (999, 'WEST999', 'West Hall Special', 3, ?, 60)
    """, (dept_id,))
    
    # Insert an offering for this course
    cursor.execute("""
        INSERT INTO offerings (offering_id, course_id, prof_id, semester, year)
        VALUES (999, 999, (SELECT prof_id FROM professors LIMIT 1), 'Fall', 2024)
    """)
    
    # Insert 5 enrollments for this offering
    for i in range(1, 6):
        cursor.execute("""
            INSERT INTO enrollments (enrollment_id, offering_id, student_id, grade, enrollment_date)
            VALUES (?, 999, (SELECT student_id FROM students ORDER BY random() LIMIT 1), 'A', '2024-09-01')
        """, (9999 + i,))

    conn.commit()

# -------- Main --------
def main():
    force = "--force" in sys.argv or "--yes" in sys.argv
    # Determine project root (go up one level from scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, "test_data.db")

    if os.path.exists(db_path) and not force:
        print(f"Database already exists at {db_path}. Overwrite? (y/n)")
        if input().strip().lower() != 'y':
            print("Aborting.")
            sys.exit(0)
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    populate_database(conn)
    conn.close()

    # Print summary
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for table in ["departments", "professors", "students", "courses", "offerings", "enrollments"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cursor.fetchone()[0]}")
    conn.close()
    print(f"\n✅ Test database built at {db_path}")

if __name__ == "__main__":
    main()