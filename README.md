![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerised-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)



🏢 HRIS Database Engineering Project
📌 Project Overview

This project is a production-style Human Resources Information System (HRIS) built from scratch using modern database engineering principles.

It demonstrates:

Relational schema design

Referential integrity enforcement

Advanced PostgreSQL constraints

Synthetic data generation with Python

Bulk data loading using COPY

Containerised database deployment with Docker

Performance validation using EXPLAIN ANALYZE

The goal of this project is to move beyond academic SQL usage and demonstrate real-world database engineering discipline.

🧰 Technology Stack
Component	Technology
Database	PostgreSQL 16
Containerisation	Docker
Data Generation	Python + Faker
Data Loading	psycopg (COPY)
Version Control	Git + GitHub
Advanced Constraints	GiST + Exclusion Constraints
🏗 System Architecture
Docker (Postgres Container)
        ↓
Schema (DDL Scripts)
        ↓
Python Faker Generator
        ↓
Bulk Load via COPY
        ↓
Constraints + Indexing
        ↓
Performance Validation

🗄 Database Schema
Core Entities

Departments

Roles

Employees

Employee Roles (Many-to-Many)

Employment Contracts

Salary History

Leave Requests

Performance Reviews

🔗 Relationship Highlights

Each Role belongs to a Department

Each Employee has one primary role (optionally secondary)

Each Employee has one active contract (historical allowed)

Each Department has a manager (must belong to that department)

Salary periods cannot overlap per employee

Leave end dates must be ≥ start dates

🔐 Data Integrity & Engineering Features
✅ Referential Integrity

Foreign key constraints prevent orphan records

Manager must belong to their department

**✅ Logical Constraints**
CHECK (salary_amount > 0)
CHECK (end_date >= start_date)

**✅ Unique Constraints**
UNIQUE (department_id, title)

**✅ Advanced Exclusion Constraint (PostgreSQL Feature)**

Prevents overlapping salary periods:

EXCLUDE USING gist (
  employee_id WITH =,
  daterange(effective_from, COALESCE(effective_to, 'infinity'::date), '[]') WITH &&
);


This demonstrates real-world temporal data modelling.

**⚡ Performance & Optimisation**
Example Query
EXPLAIN ANALYZE
SELECT e.employee_id, e.full_name, r.title, d.name
FROM employees e
JOIN employee_roles er ON er.employee_id = e.employee_id
JOIN roles r ON r.role_id = er.role_id
JOIN departments d ON d.department_id = r.department_id
WHERE er.is_primary = true;

Index Strategy
CREATE INDEX ix_roles_department ON roles(department_id);
CREATE INDEX ix_employee_roles_employee ON employee_roles(employee_id);
CREATE INDEX ix_salary_employee ON salary_history(employee_id);

**📊 Synthetic Data Generation**

Data is generated using Python + Faker (en_AU locale).

Generated volumes:

1,000 Employees

45 Roles

2,978 Salary Records

4,169 Leave Requests

2,451 Performance Reviews

Generation ensures:

Valid foreign keys

No salary overlaps

Realistic employment timelines

Valid department-manager relationships

🚀 How To Run
**1️⃣ Start PostgreSQL Container**
docker compose up -d

**2️⃣ Apply Schema**
docker exec -it hris_postgres psql -U postgres -d hris -f /sql/01_tables.sql
docker exec -it hris_postgres psql -U postgres -d hris -f /sql/02_constraints.sql
docker exec -it hris_postgres psql -U postgres -d hris -f /sql/03_indexes.sql

**3️⃣ Generate Synthetic Data**
.\.venv\Scripts\python.exe python/generate_data.py

**4️⃣ Load Data into PostgreSQL**
.\.venv\Scripts\python.exe python/load_data.py

**5️⃣ Verify Data**
SELECT COUNT(*) FROM employees;

📸 Screenshots

(Create an /images folder and add screenshots)

Example markdown references:

![Tables Overview](images/tables_overview.png)
![Salary Exclusion Constraint](images/salary_constraint.png)
![EXPLAIN ANALYZE Output](images/explain_output.png)


Recommended screenshots:

\dt table list

Salary exclusion constraint applied

Manager validation query

EXPLAIN ANALYZE output

**🧠 Engineering Concepts Demonstrated**

Normalised relational modelling

Many-to-many relationship design

Window functions (row_number())

Exclusion constraints for temporal integrity

Docker-based reproducible environments

Idempotent bulk loading

Referential integrity validation queries

Query performance analysis

**🔮 Future Enhancements**

Enforce only one active primary role per employee

Add audit logging via triggers

Implement Slowly Changing Dimensions (Type 2)

Partition salary_history by year

Add CI pipeline to auto-run schema validation

**🎯 Why This Project Matters**

This project demonstrates the transition from:

“I can write SQL queries”

to

“I can design, enforce, and maintain a production-grade relational database system.”

It reflects real-world database engineering practices used in enterprise HR systems.