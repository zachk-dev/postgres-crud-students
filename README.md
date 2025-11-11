# PostgreSQL CRUD • Students Table

A minimal example showing how to:
- Create a `students` table (with identity PK + unique email)
- Seed initial data
- Run a Python app that performs all CRUD operations

## Tech
- PostgreSQL 14+/15+
- Python 3.10+ (psycopg2, python-dotenv)

## 1) Database Setup

1. Create a database (e.g., `students_db`):
   ```bash
   createdb students_db