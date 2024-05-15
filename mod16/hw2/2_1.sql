SELECT 'customer'.full_name, 'manager'.full_name, 'order'.purchase_amount, 'order'.date
FROM 'customer', 'manager', 'order'
ON 'order'.customer_id = 'customer'.customer_id AND
'order'.manager_id = 'manager'.manager_id