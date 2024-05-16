SELECT avg(assignments_grades.grade) as avg_grade, teachers.full_name
FROM assignments_grades
INNER JOIN assignments ON assignments_grades.assisgnment_id = assignments.assisgnment_id
INNER JOIN teachers ON teachers.teacher_id =assignments.teacher_id
GROUP BY teachers.teacher_id
ORDER BY avg_grade DESC
LIMIT 1