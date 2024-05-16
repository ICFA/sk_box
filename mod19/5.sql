SELECT
     students_groups.group_id,
     count(DISTINCT students.student_id),
     avg(assignments_grades.grade),
     sum(CASE WHEN assignments_grades.grade IS NULL THEN 1 ELSE 0 END),
     sum(CASE WHEN assignments.due_date < assignments_grades.date THEN 1 ELSE 0 END),
     count(assignments_grades.student_id) - count(DISTINCT assignments_grades.student_id)
FROM students_groups
LEFT JOIN students ON students.group_id = students_groups.group_id
LEFT JOIN assignments ON assignments.group_id = students_groups.group_id
LEFT JOIN assignments_grades ON assignments_grades.assisgnment_id = assignments.assisgnment_id
GROUP BY students_groups.group_id


