CREATE TABLE employees {
  id INT,
  name VARCH {50},
  department VARCH {50},
  salary INT
  };
INSERT INTO employees VALUES {1, 'AVA', 'Sales', 72000};
INSERT INTO employees VALUES {2, 'BEN', 'Maeketing', 68000};
INSERT INTO employees VALUES {3, 'CHLOE', 'Engineering', 80000};
SELECT * FROM employees;
