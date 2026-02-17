import os
import psycopg
from psycopg import sql

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "hris")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

CONNINFO = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"


def copy_csv(cur, table_name: str, filename: str, columns: list[str]):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8") as f:
        # COPY ... FROM STDIN WITH CSV HEADER
        stmt = sql.SQL("COPY {} ({}) FROM STDIN WITH (FORMAT csv, HEADER true)").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, columns))
        )
        with cur.copy(stmt) as copy:
            for line in f:
                copy.write(line)


def main():
    with psycopg.connect(CONNINFO) as conn:
        conn.autocommit = False
        with conn.cursor() as cur:
            # Clean load order: delete child tables first
            cur.execute("TRUNCATE TABLE performance_reviews RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE leave_requests RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE salary_history RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE employment_contracts RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE employee_roles RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE roles RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE employees RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE departments RESTART IDENTITY CASCADE;")
            conn.commit()

            # Load in FK-safe order
            copy_csv(cur, "departments", "departments.csv",
                     ["department_id", "name", "manager_employee_id"])
            copy_csv(cur, "roles", "roles.csv",
                     ["role_id", "department_id", "title", "is_active"])
            copy_csv(cur, "employees", "employees.csv",
                     ["employee_id", "full_name", "date_of_birth", "address_line1", "address_suburb",
                      "address_state", "address_postcode", "tfn_last4", "tfn_hash", "is_active"])
            copy_csv(cur, "employee_roles", "employee_roles.csv",
                     ["employee_id", "role_id", "is_primary", "start_date", "end_date"])
            copy_csv(cur, "employment_contracts", "employment_contracts.csv",
                     ["contract_id", "employee_id", "start_date", "end_date", "employment_type", "hours_per_week"])
            copy_csv(cur, "salary_history", "salary_history.csv",
                     ["salary_history_id", "employee_id", "department_id", "salary_amount", "effective_from", "effective_to"])
            copy_csv(cur, "leave_requests", "leave_requests.csv",
                     ["leave_request_id", "employee_id", "start_date", "end_date", "leave_type", "status"])
            copy_csv(cur, "performance_reviews", "performance_reviews.csv",
                     ["review_id", "employee_id", "review_date", "score", "comments", "reviewing_department_id", "employee_department_id"])

            conn.commit()
            print("Loaded all CSVs into Postgres successfully.")


if __name__ == "__main__":
    main()
