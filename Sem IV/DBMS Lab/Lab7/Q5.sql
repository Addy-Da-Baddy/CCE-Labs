SET SERVEROUTPUT ON;
DECLARE
    CURSOR avg_damage_cur IS
        SELECT a.location, AVG(p.damage_amount) AS average_damage
        FROM ACCIDENT a
        JOIN PARTICIPATED p ON a.report_number = p.report_number
        GROUP BY a.location;

    v_location ACCIDENT.location%TYPE;
    v_average_damage NUMBER;
BEGIN
    -- Open the cursor
    OPEN avg_damage_cur;

    LOOP
        -- Fetch the cursor values
        FETCH avg_damage_cur INTO v_location, v_average_damage;

        -- Exit the loop when no more rows are found
        EXIT WHEN avg_damage_cur%NOTFOUND;

        -- Output the results
        DBMS_OUTPUT.PUT_LINE('LOCATION: ' || v_location || ' AVERAGE_DAMAGE: ' || v_average_damage);
    END LOOP;

    -- Close the cursor
    CLOSE avg_damage_cur;
END;
/
