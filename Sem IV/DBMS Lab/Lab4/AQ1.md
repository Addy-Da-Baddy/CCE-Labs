 # On `Order Processing` database

### i) Display the names of the customers who have purchased items on 09/05/2015.

```sql
SELECT distinct c.cname 
FROM Customer c NATURAL JOIN orders o
where o.odate = TO_DATE('2025-05-09','YYYY-MM-DD');
```

### ii) Count total number of items in each order

```sql
SELECT o.ORD_NUM, SUM(oi.qty) AS total_qty
FROM ORDER_ITEMS oi
JOIN ORDERS o ON oi.order_num = o.ORD_NUM
GROUP BY o.ORD_NUM;

```

### iii) Find the order with maximum number of items in it

```sql
SELECT o.ORD_NUM, SUM(oi.qty) AS total_qty
FROM ORDER_ITEMS oi
JOIN ORDERS o ON oi.order_num = o.ORD_NUM
GROUP BY o.ORD_NUM
HAVING SUM(oi.qty) = (
    SELECT MAX(total_qty)
    FROM (
        SELECT SUM(oi.qty) AS total_qty
        FROM ORDER_ITEMS oi
        JOIN ORDERS o ON oi.order_num = o.ORD_NUM
        GROUP BY o.ORD_NUM
    )
);
```

 
### iv) Find the date on which maximum number of orders were shipped

```sql
SELECT s.shipdate, COUNT(*) AS num_orders_shipped
FROM SHIPMENT s
GROUP BY s.shipdate
HAVING COUNT(*) = (
    SELECT MAX(order_count)
    FROM (
        SELECT COUNT(*) AS order_count
        FROM SHIPMENT
        GROUP BY shipdate
    )
)
ORDER BY s.shipdate;
```

### vi) List the order no for the orders that were shipped from all the warehouses that the company has in a specific city (Kolkata)

```sql
SELECT s.order_num
FROM shipment s
WHERE NOT EXISTS (
    SELECT w.warehouse_num
    FROM warehouse w
    WHERE w.city = 'Kolkata'
    MINUS
    SELECT s2.warehouse_num
    FROM shipment s2
    WHERE s2.order_num = s.order_num
);


```


### vii)List the customer with a specific surname.


```sql
SELECT cname
FROM customer
WHERE cname LIKE '%Gupta';
```

### viii) List the customers in descending order of their total order amount.



```sql
SELECT c.cust_num, c.cname, SUM(o.ordamt) AS total_order_amount
FROM customer c
JOIN orders o ON c.cust_num = o.cust_num
GROUP BY c.cust_num, c.cname
ORDER BY total_order_amount DESC;
```


### ix)  Identify the customer with at least three orders that shipped on the particular date


```sql
SELECT c.cust_num, c.cname, COUNT(*) AS order_count
FROM customer c
JOIN orders o ON c.cust_num = o.cust_num
JOIN shipment s ON o.order_num = s.order_num
WHERE s.shipdate = TO_DATE('2025-01-06', 'YYYY-MM-DD')
GROUP BY c.cust_num, c.cname
HAVING COUNT(*) >= 3;
```
