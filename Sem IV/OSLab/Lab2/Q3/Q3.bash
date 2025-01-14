#!/bin/bash

# i) Display the number of students (only count) belonging to ICT department.
# Using grep to filter students from the ICT department and wc to count the number of lines.
echo "i) Number of students in ICT department:"
grep -c ":ICT:" studentInformation.txt
echo ""

# ii) Replace all occurrences of IT branch with "Information Technology" and save the output to ITStudents.txt
# Using sed to replace "IT" with "Information Technology" and redirecting the output to ITStudents.txt
echo "ii) Replacing 'IT' with 'Information Technology' and saving to ITStudents.txt:"
sed 's/:IT:/Information Technology/g' studentInformation.txt > ITStudents.txt
echo "Output saved to ITStudents.txt"
echo ""

# iii) Display the average marks of a student with the given registration number "1234"
# Using grep to find the line with the given registration number, then using awk to calculate the average.
echo "iii) Average marks for student with Registration No. 1234:"
grep "^1234" studentInformation.txt | awk -F ':' '{ avg=($6+$7+$8)/3; print avg }'
echo ""

# iv) Display the title row in uppercase. The remaining lines should be unchanged.
# Using sed to convert only the first line (title row) to uppercase, keeping other lines unchanged.
echo "iv) Title row in uppercase, remaining lines unchanged:"
sed '1s/.*/\U&/' studentInformation.txt

