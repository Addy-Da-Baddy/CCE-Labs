-- Identify all drivers who have never been involved in any accidents.

CREATE OR REPLACE PROCEDURE get_drivers_not_involved_in_accidents
IS
    v_count NUMBER := 0;  
BEGIN
    FOR rec IN
    (
        SELECT DRIVER_ID, NAME, ADDRESS
        FROM Person  
        WHERE DRIVER_ID NOT IN (SELECT DRIVER_ID FROM Participated)  
    )
    LOOP
        DBMS_OUTPUT.PUT_LINE('Driver ID: ' || rec.DRIVER_ID ||
                             ', Name: ' || rec.NAME ||
                             ', Address: ' || rec.ADDRESS);
        v_count := v_count + 1; 
    END LOOP;

    IF v_count = 0 THEN
        DBMS_OUTPUT.PUT_LINE('No drivers found who have never been involved in any accidents.');
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('An error occurred: ' || SQLERRM);
END get_drivers_not_involved_in_accidents;
/



BEGIN
    get_drivers_not_involved_in_accidents;
END;
/
