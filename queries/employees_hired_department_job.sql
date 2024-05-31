/*
Number of employees hired for each job and department in 2021 divided by quarter. The
table must be ordered alphabetically by department and job.
*/

SELECT 
  d.department,
  j.jobs,
  SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
  SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
  SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
  SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 4 THEN 1 ELSE 0 END) AS Q4

FROM `HRDB.department` d
INNER JOIN `HRDB.hired_employees` he
ON d.id = he.department_id
INNER JOIN `HRDB.jobs` j
ON he.job_id = j.id
WHERE EXTRACT(YEAR FROM he.datetime) = 2021
GROUP BY 1, 2
ORDER BY 1 asc, 2 asc

/*
department,jobs,Q1,Q2,Q3,Q4
Accounting,Account Representative IV,1,0,0,0
*/