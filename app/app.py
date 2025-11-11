"""
PostgreSQL CRUD demo for the 'students' table.

Functions:
- getAllStudents(): prints all student rows
- addStudent(first_name, last_name, email, enrollment_date): inserts a student
- updateStudentEmail(student_id, new_email): updates a student's email
- deleteStudent(student_id): deletes a student by id

Run:
  python app.py get-all
  python app.py add --first "Alice" --last "Wong" --email "alice@x.com" --date 2024-09-01
  python app.py update-email --id 1 --email "johnny.doe@example.com"
  python app.py delete --id 3
"""

import os
import argparse
import psycopg
from psycopg.rows import dict_row
from psycopg.errors import UniqueViolation
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

def get_conn():
    """
    Opens a PostgreSQL connection using environment variables.
    Prefers PG* vars; falls back to your macOS username for user.
    """
    return psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "students_db"),
        user=os.getenv("PGUSER", os.getenv("USER", "")),
        password=os.getenv("PGPASSWORD", ""),
    )

def getAllStudents():
    """
    Retrieves and prints all student records.
    """
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            SELECT student_id, first_name, last_name, email, enrollment_date
            FROM students
            ORDER BY student_id;
        """)
        rows = cur.fetchall()
    if not rows:
        print("No students found.")
        return
    print("student_id | first_name | last_name | email                     | enrollment_date")
    print("-----------+------------+-----------+---------------------------+----------------")
    for r in rows:
        date_str = r["enrollment_date"].isoformat() if r["enrollment_date"] else ""
        print(f'{r["student_id"]:>10} | {r["first_name"]:<10} | {r["last_name"]:<9} | {r["email"]:<25} | {date_str}')

def addStudent(first_name: str, last_name: str, email: str, enrollment_date: str):
    """
    Inserts a new student record. enrollment_date must be YYYY-MM-DD (or omit/empty).
    """
    date_val = None
    if enrollment_date:
        try:
            date_val = datetime.strptime(enrollment_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("enrollment_date must be YYYY-MM-DD")

    sql = """
        INSERT INTO students (first_name, last_name, email, enrollment_date)
        VALUES (%s, %s, %s, %s)
        RETURNING student_id;
    """
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (first_name, last_name, email, date_val))
            new_id = cur.fetchone()[0]
        print(f"Inserted student_id={new_id}")
    except UniqueViolation:
        print("Error: email must be unique. That email already exists.")
    except Exception as e:
        print(f"Insert failed: {e}")

def updateStudentEmail(student_id: int, new_email: str):
    """
    Updates the email for a given student_id.
    """
    sql = """
        UPDATE students
        SET email = %s
        WHERE student_id = %s;
    """
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (new_email, student_id))
            if cur.rowcount == 0:
                print(f"No student found with id {student_id}.")
            else:
                print(f"Updated student_id={student_id} email -> {new_email}")
    except UniqueViolation:
        print("Error: email must be unique. That email already exists.")
    except Exception as e:
        print(f"Update failed: {e}")

def deleteStudent(student_id: int):
    """
    Deletes the record for the given student_id.
    """
    sql = "DELETE FROM students WHERE student_id = %s;"
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (student_id,))
            if cur.rowcount == 0:
                print(f"No student found with id {student_id}.")
            else:
                print(f"Deleted student_id={student_id}")
    except Exception as e:
        print(f"Delete failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Students CRUD app")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("get-all", help="List all students")

    p_add = sub.add_parser("add", help="Add a student")
    p_add.add_argument("--first", required=True)
    p_add.add_argument("--last", required=True)
    p_add.add_argument("--email", required=True)
    p_add.add_argument("--date", default="", help="YYYY-MM-DD (optional)")

    p_upd = sub.add_parser("update-email", help="Update a student's email")
    p_upd.add_argument("--id", type=int, required=True)
    p_upd.add_argument("--email", required=True)

    p_del = sub.add_parser("delete", help="Delete a student by id")
    p_del.add_argument("--id", type=int, required=True)

    args = parser.parse_args()

    if args.cmd == "get-all":
        getAllStudents()
    elif args.cmd == "add":
        addStudent(args.first, args.last, args.email, args.date)
    elif args.cmd == "update-email":
        updateStudentEmail(args.id, args.email)
    elif args.cmd == "delete":
        deleteStudent(args.id)

if __name__ == "__main__":
    main()