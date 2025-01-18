
# Additional Question 1

## i. Create the Tables


```sql
CREATE TABLE CUSTOMER (
    cust_num INT PRIMARY KEY,
    cname VARCHAR(50),
    city VARCHAR(30)
);

CREATE TABLE ORDERS (
    order_num INT PRIMARY KEY,
    odate DATE,
    cust_num INT,
    ordamt INT,
    FOREIGN KEY (cust_num) REFERENCES CUSTOMER(cust_num)
);

CREATE TABLE ITEM (
    item_num INT PRIMARY KEY,
    unitprice INT
);

CREATE TABLE ORDER_ITEMS (
    order_num INT,
    qty INT,
    item_num INT,
    PRIMARY KEY (order_num, item_num),
    FOREIGN KEY (order_num) REFERENCES ORDERS(order_num),
    FOREIGN KEY (item_num) REFERENCES ITEM(item_num)
);


CREATE TABLE WAREHOUSE (
    warehouse_num INT PRIMARY KEY,
    city VARCHAR(30)
);

CREATE TABLE SHIPMENT (
    order_num INT,
    warehouse_num INT,
    shipdate DATE,
    PRIMARY KEY (order_num, warehouse_num),
    FOREIGN KEY (order_num) REFERENCES ORDERS(order_num)
    FOREIGN KEY (warehouse_num_num) REFERENCES WAREHOUSE(warehouse_num)
);


```

## ii. Insert Data


```sql
-- CUSTOMER data
INSERT INTO CUSTOMER (cust_num, cname, city)
VALUES
(1, 'Alice', 'New York'),
(2, 'Bob', 'Los Angeles'),
(3, 'Charlie', 'Chicago'),
(4, 'David', 'Houston'),
(5, 'Eva', 'Phoenix');

-- ORDERS data
INSERT INTO ORDERS (order_num, odate, cust_num, ordamt)
VALUES
(101, '2025-01-01', 1, 200),
(102, '2025-01-02', 2, 500),
(103, '2025-01-03', 3, 700),
(104, '2025-01-04', 4, 300),
(105, '2025-01-05', 5, 400);

-- ITEM data
INSERT INTO ITEM (item_num, unitprice)
VALUES
(1001, 20),
(1002, 50),
(1003, 30),
(1004, 80),
(1005, 60);

-- ORDER_ITEMS data
INSERT INTO ORDER_ITEMS (order_num, qty, item_num)
VALUES
(101, 5, 1001),
(102, 12, 1002),
(103, 7, 1003),
(104, 15, 1004),
(105, 9, 1005);


-- SHIPMENT data
INSERT INTO SHIPMENT (order_num, warehouse_num, shipdate)
VALUES
(101, 201, '2025-01-06'),
(102, 202, '2025-01-07'),
(103, 203, '2025-01-08'),
(104, 204, '2025-01-09'),
(105, 205, '2025-01-10');

-- WAREHOUSE data
INSERT INTO WAREHOUSE (warehouse_num, city)
VALUES
(201, 'New York'),
(202, 'Los Angeles'),
(203, 'Chicago'),
(204, 'Houston'),
(205, 'Phoenix');


```

## iii. Queries

### a. Produce a Listing: CUSTNAME, No. of Orders, AVG_ORDER_AMT


```sql
SELECT 
    C.cname AS CUSTNAME,
    COUNT(O.order_num) AS No_of_Orders,
    AVG(O.ordamt) AS AVG_ORDER_AMT
FROM 
    CUSTOMER C
LEFT JOIN 
    ORDERS O ON C.cust_num = O.cust_num
GROUP BY 
    C.cust_num, C.cname;
```

### b. List the Order Numbers for Orders Shipped from All Warehouses in a Specific City


```sql
SELECT DISTINCT S.order_num
FROM SHIPMENT S
JOIN WAREHOUSE W ON S.warehouse_num = W.warehouse_num
WHERE W.city = 'New York';
```

### c. Decrease the Order Amount Based on Quantity Ordered



```sql
UPDATE ORDERS O
SET O.ordamt = O.ordamt * 
    CASE
        WHEN (SELECT SUM(oi.qty) FROM ORDER_ITEMS oi WHERE oi.order_num = O.order_num) > 10 THEN 0.9
        ELSE 0.95
    END;
```
