import csv
import os 
import random
import hashlib
from datetime import date, timedelta

from faker import Faker

fake = Faker("en_AU")
random.seed(42)
Faker.seed(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)

DEPARTMENTS_N = 12
ROLES_PER_DEPT_MIN = 3
ROLES_PER_DEPT_MAX = 7
EMPLOYEES_N = 1000

SECOND_ROLE_PROB = 0.10

LEAVE_MAX_PER_EMP = 8
REVIEWS_MAX_PER_EMP = 6
SALARY_MAX_CHANGES = 6

EMPLOYMENT_TYPES = ["FT", "PT", "Casual"]
LEAVE_TYPES = ["Annual", "Sick", "Carer", "Long Service", "Unpaid"]
LEAVE_STATUS = ["SUBMITTED", "APPROVED", "REJECTED", "CANCELLED"]

STATES = ["TAS", "VIC", "NSW", "QLD", "SA", "WA", "ACT", "NT"]

def rand_date(start: date, end: date) -> date:
    """Random date between start and end (inclusive)."""
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 0)))


def fake_tfn() -> str:
    # 9-digit fake TFN (not valid, just format)
    return "".join(str(random.randint(0, 9)) for _ in range(9))


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def main():
    # 1) Departments
    dept_names = [
        "People & Culture", "Finance", "IT", "Operations", "Sales", "Marketing",
        "Customer Service", "Risk & Compliance", "Legal", "Data & Analytics",
        "Facilities", "Procurement"
    ]
    dept_names = dept_names[:DEPARTMENTS_N]

    departments = []
    for i, name in enumerate(dept_names, start=1):
        departments.append({
            "department_id": i,
            "name": name,
            "manager_employee_id": ""  # fill later once employees exist
        })

    # 2) Roles
    role_titles_by_dept = {
        "People & Culture": ["HR Officer", "HR Adviser", "Recruiter", "HR Analyst", "P&C Coordinator"],
        "Finance": ["Accounts Officer", "Payroll Officer", "Financial Analyst", "Finance Manager"],
        "IT": ["Service Desk Analyst", "Systems Admin", "DBA", "Network Engineer", "Security Analyst"],
        "Operations": ["Operations Coordinator", "Operations Analyst", "Team Leader"],
        "Sales": ["Account Executive", "Sales Development Rep", "Sales Manager"],
        "Marketing": ["Marketing Coordinator", "Digital Marketer", "Content Specialist"],
        "Customer Service": ["Customer Support Officer", "Senior Support Officer", "Team Leader"],
        "Risk & Compliance": ["Compliance Officer", "Risk Analyst", "Assurance Officer"],
        "Legal": ["Legal Assistant", "Paralegal", "Legal Counsel"],
        "Data & Analytics": ["Data Analyst", "BI Developer", "Data Engineer", "Analytics Manager"],
        "Facilities": ["Facilities Officer", "Workplace Coordinator"],
        "Procurement": ["Procurement Officer", "Buyer", "Vendor Manager"],
    }

    roles = []
    role_id = 1
    for dept in departments:
        dept_id = dept["department_id"]
        dept_name = dept["name"]
        base_titles = role_titles_by_dept.get(dept_name, ["Officer", "Analyst", "Manager"])
        n_roles = random.randint(ROLES_PER_DEPT_MIN, ROLES_PER_DEPT_MAX)

        # ensure uniqueness per dept by title; vary with level suffixes if needed
        titles = []
        while len(titles) < n_roles:
            t = random.choice(base_titles)
            if random.random() < 0.25:
                t = f"Senior {t}"
            if random.random() < 0.10:
                t = f"{t} (Contract)"
            if t not in titles:
                titles.append(t)

        for title in titles:
            roles.append({
                "role_id": role_id,
                "department_id": dept_id,
                "title": title,
                "is_active": "true",
            })
            role_id += 1

    # Helper: roles by department
    roles_by_dept = {}
    for r in roles:
        roles_by_dept.setdefault(r["department_id"], []).append(r["role_id"])

    # 3) Employees
    employees = []
    employee_roles = []
    contracts = []
    salary_history = []
    leave_requests = []
    performance_reviews = []

    today = date.today()
    earliest_start = today - timedelta(days=3650)  # ~10 years
    adult_min_dob = today - timedelta(days=365 * 65)
    adult_max_dob = today - timedelta(days=365 * 18)

    for emp_id in range(1, EMPLOYEES_N + 1):
        name = fake.name()
        dob = rand_date(adult_min_dob, adult_max_dob)

        suburb = fake.city()
        state = random.choice(STATES)
        postcode = fake.postcode()

        tfn = fake_tfn()
        employees.append({
            "employee_id": emp_id,
            "full_name": name,
            "date_of_birth": dob.isoformat(),
            "address_line1": fake.street_address(),
            "address_suburb": suburb,
            "address_state": state,
            "address_postcode": postcode,
            "tfn_last4": tfn[-4:],
            "tfn_hash": sha256_hex(tfn),
            "is_active": "true",
        })

        # Choose a primary department + role
        dept_id = random.choice(departments)["department_id"]
        primary_role_id = random.choice(roles_by_dept[dept_id])
        employee_roles.append({
            "employee_id": emp_id,
            "role_id": primary_role_id,
            "is_primary": "true",
            "start_date": rand_date(earliest_start, today - timedelta(days=14)).isoformat(),
            "end_date": "",
        })

        # Optional secondary role (could be in same dept or different)
        if random.random() < SECOND_ROLE_PROB:
            dept2 = dept_id if random.random() < 0.6 else random.choice(departments)["department_id"]
            role2 = random.choice(roles_by_dept[dept2])
            if role2 != primary_role_id:
                employee_roles.append({
                    "employee_id": emp_id,
                    "role_id": role2,
                    "is_primary": "false",
                    "start_date": rand_date(earliest_start, today - timedelta(days=14)).isoformat(),
                    "end_date": "",
                })

        # Contract (1 per employee for now)
        start_date = rand_date(earliest_start, today - timedelta(days=14))
        contracts.append({
            "contract_id": emp_id,  # simple deterministic id
            "employee_id": emp_id,
            "start_date": start_date.isoformat(),
            "end_date": "",
            "employment_type": random.choice(EMPLOYMENT_TYPES),
            "hours_per_week": str(random.choice([38, 40, 36, 30, 20, 15])) if random.random() < 0.9 else "",
        })

        # Salary history: 1..SALARY_MAX_CHANGES, non-overlapping effective dates
        changes = random.randint(1, SALARY_MAX_CHANGES)
        effective_from = start_date
        base_salary = random.randint(55000, 140000)

        for j in range(changes):
            # each change lasts 90..540 days (rough)
            duration_days = random.randint(90, 540)
            effective_to = effective_from + timedelta(days=duration_days)
            if effective_to > today:
                effective_to = None

            salary_amount = base_salary + (j * random.randint(1000, 7000))
            salary_history.append({
                "salary_history_id": len(salary_history) + 1,
                "employee_id": emp_id,
                "department_id": dept_id,
                "salary_amount": f"{salary_amount:.2f}",
                "effective_from": effective_from.isoformat(),
                "effective_to": "" if effective_to is None else effective_to.isoformat(),
            })

            if effective_to is None:
                break
            effective_from = effective_to + timedelta(days=1)

        # Leave requests: 0..LEAVE_MAX_PER_EMP
        for _ in range(random.randint(0, LEAVE_MAX_PER_EMP)):
            ls = rand_date(start_date, today)
            le = ls + timedelta(days=random.randint(1, 14))
            if le > today + timedelta(days=60):  # allow some future requests
                le = today + timedelta(days=random.randint(1, 60))
            leave_requests.append({
                "leave_request_id": len(leave_requests) + 1,
                "employee_id": emp_id,
                "start_date": ls.isoformat(),
                "end_date": le.isoformat(),
                "leave_type": random.choice(LEAVE_TYPES),
                "status": random.choice(LEAVE_STATUS),
            })

        # Reviews: 0..REVIEWS_MAX_PER_EMP, only if employed long enough
        employed_days = (today - start_date).days
        possible_reviews = min(REVIEWS_MAX_PER_EMP, max(0, employed_days // 180))
        for _ in range(random.randint(0, possible_reviews)):
            rd = rand_date(start_date + timedelta(days=30), today)
            score = round(random.uniform(2.0, 5.0), 2)
            reviewing_dept_id = dept_id if random.random() < 0.8 else random.choice(departments)["department_id"]
            performance_reviews.append({
                "review_id": len(performance_reviews) + 1,
                "employee_id": emp_id,
                "review_date": rd.isoformat(),
                "score": f"{score:.2f}",
                "comments": fake.sentence(nb_words=12),
                "reviewing_department_id": reviewing_dept_id,
                "employee_department_id": dept_id,
            })

    # # 4) Pick department managers AFTER employees exist
    # # choose a random employee per dept (not perfect but fine)
    # for dept in departments:
    #     dept["manager_employee_id"] = str(random.randint(1, EMPLOYEES_N))

    # Write CSVs
    write_csv(os.path.join(OUT_DIR, "departments.csv"),
              ["department_id", "name", "manager_employee_id"], departments)

    write_csv(os.path.join(OUT_DIR, "roles.csv"),
              ["role_id", "department_id", "title", "is_active"], roles)

    write_csv(os.path.join(OUT_DIR, "employees.csv"),
              ["employee_id", "full_name", "date_of_birth", "address_line1", "address_suburb",
               "address_state", "address_postcode", "tfn_last4", "tfn_hash", "is_active"], employees)

    write_csv(os.path.join(OUT_DIR, "employee_roles.csv"),
              ["employee_id", "role_id", "is_primary", "start_date", "end_date"], employee_roles)

    write_csv(os.path.join(OUT_DIR, "employment_contracts.csv"),
              ["contract_id", "employee_id", "start_date", "end_date", "employment_type", "hours_per_week"], contracts)

    write_csv(os.path.join(OUT_DIR, "salary_history.csv"),
              ["salary_history_id", "employee_id", "department_id", "salary_amount", "effective_from", "effective_to"], salary_history)

    write_csv(os.path.join(OUT_DIR, "leave_requests.csv"),
              ["leave_request_id", "employee_id", "start_date", "end_date", "leave_type", "status"], leave_requests)

    write_csv(os.path.join(OUT_DIR, "performance_reviews.csv"),
              ["review_id", "employee_id", "review_date", "score", "comments", "reviewing_department_id", "employee_department_id"],
              performance_reviews)

    print(f"Done. Wrote CSVs to: {os.path.abspath(OUT_DIR)}")
    print(f"Rows: departments={len(departments)}, roles={len(roles)}, employees={len(employees)}, "
          f"employee_roles={len(employee_roles)}, contracts={len(contracts)}, salary_history={len(salary_history)}, "
          f"leave_requests={len(leave_requests)}, performance_reviews={len(performance_reviews)}")


if __name__ == "__main__":
    main()
