SELECT assignment_text, avg(grade)
FROM assignments_grades
JOIN assignments ON assignments_grades.assisgnment_id = assignments.assisgnment_id
WHERE assignment_text LIKE '%прочитать%' OR assignment_text LIKE '%выучить%'
GROUP BY assignment_text