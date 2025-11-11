PostgreSQL CRUD – Students Table

This project demonstrates a simple PostgreSQL + Python application that performs full CRUD operations (Create, Read, Update, Delete) on a students table.

⸻

Objective

Implement a PostgreSQL database using the provided schema and build a Python application that connects to the database to perform CRUD operations.

⸻

Database Schema

Table Name: students

Column	Type	Constraints
student_id	Integer	Primary Key, Auto-increment
first_name	Text	Not Null
last_name	Text	Not Null
email	Text	Not Null, Unique
enrollment_date	Date	—

Initial Data:

INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');


⸻

Technologies Used
	•	PostgreSQL 14+
	•	Python 3.12+
	•	psycopg 3 (PostgreSQL adapter)
	•	python-dotenv (for environment variables)

⸻

Folder Structure

project/
├── app/
│   └── app.py              # main application file
├── db/
│   ├── schema.sql          # creates the students table
│   └── seed.sql            # inserts initial data
├── .env.example            # environment variable template
├── requirements.txt        # dependencies
└── README.md


⸻

Setup Instructions

1. Create Database

createdb students_db

2. Run SQL Scripts

psql -d students_db -f db/schema.sql
psql -d students_db -f db/seed.sql

3. Verify Data

psql -d students_db -c "SELECT * FROM students;"


⸻

Running the Application

Step 1 – Install Dependencies

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Step 2 – Configure Environment

Create a file named .env in your project root:

PGHOST=localhost
PGPORT=5432
PGDATABASE=students_db
PGUSER=z          # replace with your macOS username
PGPASSWORD=


⸻

CRUD Operations

View All Students

python app/app.py get-all

Add a Student

python app/app.py add --first "Alice" --last "Wong" --email "alice@example.com" --date 2024-09-01

Update Student Email

python app/app.py update-email --id 1 --email "johnny.doe@example.com"

Delete a Student

python app/app.py delete --id 3


Youtube video explanation
https://youtu.be/L0y5oexkjAI
