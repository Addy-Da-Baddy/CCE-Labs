-- Create a procedure to display total damage caused due to an accident for a particular driver on a specific year.

CREATE OR REPLACE PROCEDURE get_total_damage(
    p_driver_id IN VARCHAR2,
    p_year IN NUMBER
)
IS
    total_damage NUMBER := 0;
BEGIN
    SELECT SUM(DAMAGE_AMOUNT)
    INTO total_damage
    FROM Participated p
    JOIN Accident a ON p.REPORT_NUMBER = a.REPORT_NUMBER
    WHERE p.DRIVER_ID = p_driver_id
    AND EXTRACT(YEAR FROM a.ACCD_DATE) = p_year;

    DBMS_OUTPUT.PUT_LINE('Total Damage for Driver ' || p_driver_id || ' in ' || p_year || ' is: ' || total_damage);
END get_total_damage;
/


BEGIN
    get_total_damage('D001', 2022);
END;
/
