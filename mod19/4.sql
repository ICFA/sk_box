SELECT avg(overdue), max(overdue), min(overdue) FROM (
    SELECT sum(assignments_grades.date > assignments.due_date) as overdue
    FROM assignments
    INNER JOIN assignments_grades ON assignments.assisgnment_id = assignments_grades.assisgnment_id
    GROUP BY assignments.group_id)

