**Database 1: Insurance**

```sql
PERSON (driver_id#: varchar(30), name: varchar(50),
address:varchar(100)
CAR (regno: varchar(20), model: varchar(30), Year:int)
ACCIDENT (report_number: int, accd_date: date, location:
varchar(50))
OWNS (driver_id#: varchar(30), regno: varchar(20))
PARTICIPATED (driver_id#: varchar(30), regno: varchar(20), report_number:
int, damage_amount: int)```

**Database 2: Order Processing**

```sql
CUSTOMER (cust#: int, cname: varchar(50), city:
varchar(30))
ORDERS (order#:int, odate: date, cust#: int, ordamt: int)
ITEM (item#: int, unitprice: int)
ORDER_ITEMS (order#:int, qty:int, item#:int)
SHIPMENT (order#: int, warehouse#: int, shipdate: date)
WAREHOUSE (warehouse#:int, city: varchar(30))```

