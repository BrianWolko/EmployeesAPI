/*
List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending).
*/

SELECT 
  d.id,
  d.department, 
  COUNT(he.id) AS employee_count
FROM HRDB.department d
LEFT JOIN HRDB.hired_employees he 
ON d.id = he.department_id
GROUP BY d.id ,d.department
HAVING COUNT(he.id) > (SELECT AVG(count) FROM (
  SELECT COUNT(*) AS count
  FROM HRDB.hired_employees
  GROUP BY department_id
))
ORDER BY 1, 2;

