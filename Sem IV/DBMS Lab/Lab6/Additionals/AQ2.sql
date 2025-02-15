CREATE OR REPLACE PROCEDURE DISPLAY_DISCOUNTED_ORDERS IS
BEGIN
    FOR REC IN (
        SELECT O.ORDER#, O.ORDAMT, (O.ORDAMT * 0.20) AS DISCOUNT_AMOUNT
        FROM ORDERS O
        WHERE O.ORDER# IN (
            SELECT ORDER# 
            FROM ORDER_ITEMS
            GROUP BY ORDER#
            HAVING SUM(QTY) >= 5
        )
    ) LOOP
        DBMS_OUTPUT.PUT_LINE('Order#: ' || REC.ORDER# || 
                             ', Original Amount: ' || REC.ORDAMT || 
                             ', Discount (20%): ' || REC.DISCOUNT_AMOUNT ||
                             ', Final Amount: ' || (REC.ORDAMT - REC.DISCOUNT_AMOUNT));
    END LOOP;
END DISPLAY_DISCOUNTED_ORDERS;
/
