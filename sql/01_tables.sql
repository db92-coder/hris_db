BEGIN;

-- Departments
CREATE TABLE IF NOT EXISTS departments (
  department_id      BIGSERIAL PRIMARY KEY,
  name               TEXT NOT NULL UNIQUE,
  manager_employee_id BIGINT NULL, -- FK added after employees exists
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Roles
CREATE TABLE IF NOT EXISTS roles (
  role_id        BIGSERIAL PRIMARY KEY,
  department_id  BIGINT NOT NULL,
  title          TEXT NOT NULL,
  is_active      BOOLEAN NOT NULL DEFAULT TRUE,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT uq_roles_department_title UNIQUE (department_id, title)
);

-- Employees (no job title here; role supplies title)
CREATE TABLE IF NOT EXISTS employees (
  employee_id     BIGSERIAL PRIMARY KEY,
  full_name       TEXT NOT NULL,
  date_of_birth   DATE NOT NULL,
  address_line1   TEXT NOT NULL,
  address_suburb  TEXT NOT NULL,
  address_state   TEXT NOT NULL,
  address_postcode TEXT NOT NULL,
  tfn_last4       TEXT NULL,
  tfn_hash        TEXT NULL, -- store hashed fake TFN, not plaintext
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Employee Roles (supports 1–2 roles; can become history later)
CREATE TABLE IF NOT EXISTS employee_roles (
  employee_id   BIGINT NOT NULL,
  role_id       BIGINT NOT NULL,
  is_primary    BOOLEAN NOT NULL DEFAULT FALSE,
  start_date    DATE NOT NULL DEFAULT CURRENT_DATE,
  end_date      DATE NULL,
  PRIMARY KEY (employee_id, role_id, start_date)
);

-- Employment Contracts (one active, can be many historical)
CREATE TABLE IF NOT EXISTS employment_contracts (
  contract_id      BIGSERIAL PRIMARY KEY,
  employee_id      BIGINT NOT NULL,
  start_date       DATE NOT NULL,
  end_date         DATE NULL,
  employment_type  TEXT NOT NULL, -- FT/PT/Casual
  hours_per_week   NUMERIC(5,2) NULL,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Leave Requests
CREATE TABLE IF NOT EXISTS leave_requests (
  leave_request_id BIGSERIAL PRIMARY KEY,
  employee_id      BIGINT NOT NULL,
  start_date       DATE NOT NULL,
  end_date         DATE NOT NULL,
  leave_type       TEXT NOT NULL, -- Annual/Sick/etc
  status           TEXT NOT NULL DEFAULT 'SUBMITTED',
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT chk_leave_dates CHECK (end_date >= start_date)
);

-- Performance Reviews
CREATE TABLE IF NOT EXISTS performance_reviews (
  review_id                BIGSERIAL PRIMARY KEY,
  employee_id              BIGINT NOT NULL,
  review_date              DATE NOT NULL,
  score                    NUMERIC(4,2) NOT NULL,
  comments                 TEXT NULL,
  reviewing_department_id  BIGINT NOT NULL,
  employee_department_id   BIGINT NOT NULL,
  created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT chk_score_range CHECK (score >= 0 AND score <= 5)
);

-- Salary History (point-in-time)
CREATE TABLE IF NOT EXISTS salary_history (
  salary_history_id BIGSERIAL PRIMARY KEY,
  employee_id       BIGINT NOT NULL,
  department_id     BIGINT NOT NULL,
  salary_amount     NUMERIC(12,2) NOT NULL,
  effective_from    DATE NOT NULL,
  effective_to      DATE NULL,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT chk_salary_positive CHECK (salary_amount > 0),
  CONSTRAINT chk_salary_dates CHECK (effective_to IS NULL OR effective_to >= effective_from)
);

COMMIT;
