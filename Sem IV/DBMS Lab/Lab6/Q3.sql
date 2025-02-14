
-- Create a procedure to display accident information which took place in a particular location.

CREATE OR REPLACE PROCEDURE get_accidents_by_location(
    p_location IN VARCHAR2
)
IS
    v_count NUMBER := 0; 
BEGIN
    FOR rec IN
    (   
        SELECT REPORT_NUMBER, ACCD_DATE, LOCATION
        FROM Accident
        WHERE LOCATION = p_location
    )
    LOOP
        DBMS_OUTPUT.PUT_LINE('Report Number: ' || rec.REPORT_NUMBER || 
                             ', Date: ' || TO_CHAR(rec.ACCD_DATE, 'YYYY-MM-DD') ||
                             ', Location: ' || rec.LOCATION);
        v_count := v_count + 1; 
    END LOOP;
    
    IF v_count = 0 THEN
        DBMS_OUTPUT.PUT_LINE('No accidents found in location: ' || p_location);
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('An error occurred: ' || SQLERRM);
END get_accidents_by_location;
/


BEGIN
    get_accidents_by_location('Janpath, Delhi');
END;
/
