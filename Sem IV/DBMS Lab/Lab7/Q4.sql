SET SERVEROUTPUT ON;
DECLARE
    CURSOR car_accidents_cur IS
        SELECT p.REGNO, 
               (SELECT MODEL FROM CAR WHERE REGNO = p.REGNO) AS MODEL,
               COUNT(*) AS accident_count, 
               SUM(p.DAMAGE_AMOUNT) AS total_damage
        FROM PARTICIPATED p
        GROUP BY p.REGNO
        HAVING COUNT(*) > 1
        ORDER BY total_damage DESC;

    v_regno CAR.REGNO%TYPE;
    v_model CAR.MODEL%TYPE;
    v_accident_count NUMBER;
    v_total_damage NUMBER;
BEGIN
    -- Open the cursor
    OPEN car_accidents_cur;

    LOOP
        -- Fetch the cursor values
        FETCH car_accidents_cur INTO v_regno, v_model, v_accident_count, v_total_damage;

        -- Exit the loop when no more rows are found
        EXIT WHEN car_accidents_cur%NOTFOUND;

        -- Output the results
        DBMS_OUTPUT.PUT_LINE('REGNO: ' || v_regno || ' MODEL: ' || v_model || ' ACCIDENT_COUNT: ' || v_accident_count || ' TOTAL_DAMAGE: ' || v_total_damage);
    END LOOP;

    -- Close the cursor
    CLOSE car_accidents_cur;
END;
/
