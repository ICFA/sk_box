SELECT 'customer'.full_name
FROM 'customer'
LEFT JOIN 'order'
ON 'order'.customer_id = 'customer'.customer_id
WHERE 'order'.customer_id IS NULL
