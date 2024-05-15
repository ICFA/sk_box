SELECT 'order'.order_no, 'manager'.full_name, 'customer'.full_name
FROM 'customer', 'manager', 'order'
ON 'order'.customer_id = 'customer'.customer_id AND
'order'.manager_id = 'manager'.manager_id AND
'manager'.city != 'customer'.city