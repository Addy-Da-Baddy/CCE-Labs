**Database 1: Insurance**

```sql
PERSON (driver_id#: varchar(30), name: varchar(50),
address:varchar(100)
CAR (regno: varchar(20), model: varchar(30), Year:int)
ACCIDENT (report_number: int, accd_date: date, location:
varchar(50))
OWNS (driver_id#: varchar(30), regno: varchar(20))
PARTICIPATED (driver_id#: varchar(30), regno: varchar(20), report_number:
int, damage_amount: int)
```

**Database 2: Order Processing**

```sql
CUSTOMER (cust#: int, cname: varchar(50), city:
varchar(30))
ORDERS (order#:int, odate: date, cust#: int, ordamt: int)
ITEM (item#: int, unitprice: int)
ORDER_ITEMS (order#:int, qty:int, item#:int)
SHIPMENT (order#: int, warehouse#: int, shipdate: date)
WAREHOUSE (warehouse#:int, city: varchar(30))
```

**Database 3: Student Enrollment**

```sql
STUDENT (regno: varchar(20), name: varchar(50), major: varchar(20),
bdate:date)
COURSE (course#:int, cname: varchar(30), dept: varchar(30))
ENROLL (regno: varchar(20), course#:int, sem:int,
book_isbn:int)
BOOK_ADOPTION (course#:int, sem:int, book_isbn:int)
TEXT (book_isbn:int, booktitle: varchar(50), publisher: varchar(50), author:
varchar(50))
```

SELECT b.book_isbn, b.booktitle
FROM TEXT b
WHERE b.book_isbn IN (
    SELECT ba.book_isbn
    FROM BOOK_ADOPTION ba
    WHERE ba.course_num IN (
        SELECT e.course_num
        FROM ENROLL e
        WHERE e.book_isbn = ba.book_isbn
    )
);

