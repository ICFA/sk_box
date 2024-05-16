SELECT avg(assignments_grades.grade) as avg_grade, students.full_name
FROM assignments_grades
INNER JOIN students ON assignments_grades.student_id = students.student_id
GROUP BY students.student_id
ORDER BY avg_grade DESC
LIMIT 10;

