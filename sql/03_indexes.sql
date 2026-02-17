BEGIN;

CREATE INDEX IF NOT EXISTS ix_roles_department ON roles(department_id);

CREATE INDEX IF NOT EXISTS ix_employee_roles_employee ON employee_roles(employee_id);
CREATE INDEX IF NOT EXISTS ix_employee_roles_role ON employee_roles(role_id);

CREATE INDEX IF NOT EXISTS ix_contracts_employee ON employment_contracts(employee_id);

CREATE INDEX IF NOT EXISTS ix_leave_employee ON leave_requests(employee_id);
CREATE INDEX IF NOT EXISTS ix_leave_dates ON leave_requests(start_date, end_date);

CREATE INDEX IF NOT EXISTS ix_reviews_employee ON performance_reviews(employee_id);
CREATE INDEX IF NOT EXISTS ix_reviews_reviewing_dept ON performance_reviews(reviewing_department_id);

CREATE INDEX IF NOT EXISTS ix_salary_employee ON salary_history(employee_id);
CREATE INDEX IF NOT EXISTS ix_salary_effective ON salary_history(employee_id, effective_from);

COMMIT;
