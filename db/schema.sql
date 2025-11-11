-- Creates the students table using modern Postgres identity columns.
-- Primary key, NOT NULLs, and a UNIQUE constraint on email are enforced.

CREATE TABLE IF NOT EXISTS students (
  student_id       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  first_name       TEXT NOT NULL,
  last_name        TEXT NOT NULL,
  email            TEXT NOT NULL UNIQUE,
  enrollment_date  DATE
);

/*
1. Database setup
psql -lqt | grep students_db
psql -d students_db -c "\d students"
psql -d students_db -c "SELECT * FROM students;"

2. CRUD operations
- create
python app/app.py add --first "Alice" --last "Wong" --email "alice@example.com" --date 2024-09-01
psql -d students_db -c "SELECT * FROM students;"

- read
python app/app.py get-all

- update
python app/app.py update-email --id 1 --email "johnny.doe@example.com"
psql -d students_db -c "SELECT * FROM students;"

- delete
python app/app.py delete --id 3
psql -d students_db -c "SELECT * FROM students;"
*/