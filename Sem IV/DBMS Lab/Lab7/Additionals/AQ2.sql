SET SERVEROUTPUT ON;

DECLARE
    CURSOR non_owner_accidents_cur IS
        SELECT DISTINCT p.driver_id, p.regno, pe.name
        FROM PARTICIPATED p
        JOIN PERSON pe ON p.driver_id = pe.driver_id
        WHERE NOT EXISTS (
            SELECT 1 
            FROM OWNS o 
            WHERE o.driver_id = p.driver_id AND o.regno = p.regno
        );

BEGIN
    FOR rec IN non_owner_accidents_cur LOOP
        DBMS_OUTPUT.PUT_LINE('Driver ID: ' || rec.driver_id);
        DBMS_OUTPUT.PUT_LINE('Driver Name: ' || rec.name);
        DBMS_OUTPUT.PUT_LINE('Car Reg No: ' || rec.regno);
        DBMS_OUTPUT.PUT_LINE('-----------------------------------');
    END LOOP;
END;
/
