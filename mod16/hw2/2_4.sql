SELECT 'customer'.full_name, 'order'.order_no
FROM 'customer', 'order'
ON 'order'.customer_id = 'customer'.customer_id
WHERE 'order'.manager_id IS NULL;