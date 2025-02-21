SET SERVEROUTPUT ON;
CREATE OR REPLACE TRIGGER show_driver_info_on_accident
AFTER INSERT ON PARTICIPATED
FOR EACH ROW
DECLARE
    v_driver_name VARCHAR2(50);
    v_driver_address VARCHAR2(100);
BEGIN
    SELECT NAME, ADDRESS
    INTO v_driver_name, v_driver_address
    FROM PERSON
    WHERE DRIVER_ID =: NEW.DRIVER_ID;

    DBMS_OUTPUT.PUT_LINE('Driver Info:');
    DBMS_OUTPUT.PUT_LINE('Name: ' || v_driver_name);
    DBMS_OUTPUT.PUT_LINE('Address: ' || v_driver_address);
    DBMS_OUTPUT.PUT_LINE('Driver ID: ' || :NEW.DRIVER_ID);
    DBMS_OUTPUT.PUT_LINE('Participated in accident Report No.: ' || :NEW.REPORT_NUMBER);
END;
/
