# On `Order Processing` database

## 1. Find the customers whose address is not known yet.

```sql
SELECT cname, cust#
FROM CUSTOMER
WHERE cust# IN (
    SELECT cust#
    FROM CUSTOMER
    WHERE city IS NULL
);
```


## 2. Find the customer who has made a maximum purchase till date.

```sql
SELECT c.cust#, c.cname 
FROM CUSTOMER c 
WHERE c.cust# IN (
    SELECT o.cust# 
    FROM ORDERS o 
    WHERE o.ordamt = (
        SELECT MAX(o1.ordamt) 
        FROM ORDERS o1
    )
);

```


## 3. Display all those orders which have not been shipped yet

```sql
SELECT * 
FROM ORDERS 
WHERE order# NOT IN (
    SELECT DISTINCT order# 
    FROM SHIPMENT
);

```

## 4. Display all those orders which have not been shipped yet

```sql
SELECT distinct dept
FROM COURSE c
WHERE NOT EXISTS (
    SELECT *
    FROM BOOK_ADOPTION b
    JOIN TEXT t ON b.book_isbn = t.book_isbn
    WHERE c.course_num = b.course_num
    AND t.publisher != 'Pearson'
)
GROUP BY dept;
```

## 5. Select all those items which have not been bought by any customer.

```sql
SELECT * 
FROM ITEM 
WHERE item# NOT IN (
    SELECT DISTINCT item# 
    FROM ORDER_ITEMS
);

```
## 6. List the orders which are not shipped on a particular date.

```sql
SELECT * 
FROM ORDERS 
WHERE order# NOT IN (
    SELECT DISTINCT order# 
    FROM SHIPMENT 
    WHERE shipdate = 'YYYY-MM-DD'  -- Replace with the specific date
);

```

## 7. Identify the customers whose orders are shipped on a both specified days.
```sql
SELECT DISTINCT c.cust# , c.cname
FROM CUSTOMER c
WHERE c.cust# IN (
    SELECT o.cust# 
    FROM ORDERS o
    WHERE o.order# IN (
        SELECT s1.order#
        FROM SHIPMENT s1
        WHERE s1.shipdate = 'YYYY-MM-DD'  -- First specified date
    )
) 
AND c.cust# IN (
    SELECT o.cust# 
    FROM ORDERS o
    WHERE o.order# IN (
        SELECT s2.order#
        FROM SHIPMENT s2
        WHERE s2.shipdate = 'YYYY-MM-DD'  -- Second specified date
    )
);

```

## 8. Give the customer information whose all orders are shipped from a single warehouse

```sql
SELECT c.cust#, c.cname
FROM CUSTOMER c
WHERE NOT EXISTS (
    SELECT 1
    FROM ORDERS o
    JOIN SHIPMENT s ON o.order# = s.order#
    WHERE o.cust# = c.cust#
    AND s.warehouse# <> SPECIFIC_WAREHOUSE  -- Replace with the given warehouse#
);
```

## 9. List the customers with maximum number of orders.

```sql
SELECT c.cust#, c.cname
FROM CUSTOMER c
WHERE c.cust# IN (
    SELECT o.cust#
    FROM ORDERS o
    GROUP BY o.cust#
    HAVING COUNT(o.order#) = (
        SELECT MAX(order_count)
        FROM (
            SELECT COUNT(order#) AS order_count
            FROM ORDERS
            GROUP BY cust#
        ) AS temp
    )
);
```
