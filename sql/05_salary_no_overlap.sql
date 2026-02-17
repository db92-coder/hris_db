CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE salary_history
ADD CONSTRAINT salary_no_overlap
EXCLUDE USING gist (
  employee_id WITH =,
  daterange(effective_from, COALESCE(effective_to, 'infinity'::date), '[]') WITH &&
);
