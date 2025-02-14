-- Create a function to return total number of accidents happened in a particular year

CREATE OR REPLACE FUNCTION get_accidents_py(p_year IN NUMBER) 
RETURN NUMBER 
IS
  total_accidents NUMBER;
BEGIN
  SELECT COUNT(*)
  INTO total_accidents
  FROM Accident
  WHERE EXTRACT(YEAR FROM ACCD_DATE) = p_year;
  RETURN total_accidents;
END;
/
