BEGIN;

-- roles -> departments
ALTER TABLE roles
  ADD CONSTRAINT fk_roles_department
  FOREIGN KEY (department_id) REFERENCES departments(department_id);

-- employee_roles -> employees/roles
ALTER TABLE employee_roles
  ADD CONSTRAINT fk_employee_roles_employee
  FOREIGN KEY (employee_id) REFERENCES employees(employee_id);

ALTER TABLE employee_roles
  ADD CONSTRAINT fk_employee_roles_role
  FOREIGN KEY (role_id) REFERENCES roles(role_id);

-- contracts -> employees
ALTER TABLE employment_contracts
  ADD CONSTRAINT fk_contracts_employee
  FOREIGN KEY (employee_id) REFERENCES employees(employee_id);

-- leave -> employees
ALTER TABLE leave_requests
  ADD CONSTRAINT fk_leave_employee
  FOREIGN KEY (employee_id) REFERENCES employees(employee_id);

-- performance_reviews -> employees + departments
ALTER TABLE performance_reviews
  ADD CONSTRAINT fk_reviews_employee
  FOREIGN KEY (employee_id) REFERENCES employees(employee_id);

ALTER TABLE performance_reviews
  ADD CONSTRAINT fk_reviews_reviewing_dept
  FOREIGN KEY (reviewing_department_id) REFERENCES departments(department_id);

ALTER TABLE performance_reviews
  ADD CONSTRAINT fk_reviews_employee_dept
  FOREIGN KEY (employee_department_id) REFERENCES departments(department_id);

-- salary_history -> employees + departments
ALTER TABLE salary_history
  ADD CONSTRAINT fk_salary_employee
  FOREIGN KEY (employee_id) REFERENCES employees(employee_id);

ALTER TABLE salary_history
  ADD CONSTRAINT fk_salary_dept
  FOREIGN KEY (department_id) REFERENCES departments(department_id);

-- department manager -> employees (optional)
ALTER TABLE departments
  ADD CONSTRAINT fk_departments_manager
  FOREIGN KEY (manager_employee_id) REFERENCES employees(employee_id);

COMMIT;
