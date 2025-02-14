SET SERVEROUTPUT ON;

CREATE OR REPLACE FUNCTION ComputeArea (radius NUMBER)
RETURN NUMBER IS
    pi CONSTANT NUMBER := 3.14;  
    area NUMBER;  
BEGIN    
    area := pi * radius * radius;
    RETURN area;
END;
/

