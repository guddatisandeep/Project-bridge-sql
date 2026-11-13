-- Employee SQL practice project (fictional data).
-- Running again resets the demo table.
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary INTEGER NOT NULL CHECK (salary >= 0)
);

INSERT INTO employees (id, name, department, salary) VALUES
    (1, 'AVA', 'Sales', 72000),
    (2, 'BEN', 'Marketing', 68000),
    (3, 'CHLOE', 'Engineering', 80000);

SELECT * FROM employees;
