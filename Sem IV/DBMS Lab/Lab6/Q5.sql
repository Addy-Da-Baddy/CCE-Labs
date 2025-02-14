-- Write a function that takes a license as input and returns the total number of accidents in which the car was involved 

CREATE OR REPLACE FUNCTION get_total_accidents_by_car(
    p_regno IN VARCHAR2
) 
RETURN NUMBER
IS
    total_accidents NUMBER := 0;
BEGIN
    SELECT COUNT(*)
    INTO total_accidents
    FROM Participated
    WHERE REGNO = p_regno;
    
    RETURN total_accidents;
END get_total_accidents_by_car;
/
