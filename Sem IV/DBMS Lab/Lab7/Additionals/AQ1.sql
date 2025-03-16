SET SERVEROUTPUT ON;

CREATE OR REPLACE TRIGGER notify_driver_accident
AFTER INSERT ON PARTICIPATED
FOR EACH ROW
DECLARE
    v_accident_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_accident_count
    FROM PARTICIPATED
    WHERE driver_id = :NEW.driver_id;

    IF v_accident_count = 2 THEN
        DBMS_OUTPUT.PUT_LINE('ALERT: Driver ' || :NEW.driver_id || ' has been involved in 2 accidents!');
    END IF;
END;
/