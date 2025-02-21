
SET SERVEROUTPUT ON;
DECLARE
    CURSOR car_damage_cur IS
        SELECT c.REGNO, c.MODEL, SUM(p.DAMAGE_AMOUNT) AS TOTAL_DAMAGE
        FROM CAR c
        JOIN PARTICIPATED p ON c.REGNO = p.REGNO
        GROUP BY c.REGNO, c.MODEL
        HAVING SUM(p.DAMAGE_AMOUNT) > 4000 
        ORDER BY TOTAL_DAMAGE DESC;

    v_regno CAR.REGNO%TYPE;
    v_model CAR.MODEL%TYPE;
    v_year CAR.YEAR%TYPE;
    v_total_damage NUMBER;
BEGIN
    -- Open the cursor
    OPEN car_damage_cur;

    LOOP
        -- Fetch the cursor values
        FETCH car_damage_cur INTO v_regno, v_model, v_total_damage;

        -- Exit the loop when no more rows are found
        EXIT WHEN car_damage_cur%NOTFOUND;

        -- Output the results
        DBMS_OUTPUT.PUT_LINE('REGNO: ' || v_regno || ' MODEL: ' || v_model || ' TOTAL_DAMAGE: ' || v_total_damage);
    END LOOP;

    -- Close the cursor
    CLOSE car_damage_cur;
END;
/
