#!/bin/bash

# 1. Select lines with exactly two characters
echo "Lines with exactly two characters:"
grep '^..$' document.txt

# 2. Select lines that start with an uppercase letter
echo -e "\nLines starting with an uppercase letter:"
grep '^[A-Z]' document.txt

# 3. Select lines that end with a period
echo -e "\nLines ending with a period:"
grep '\.$' document.txt

# 4. Select lines that contain one or more blank spaces
echo -e "\nLines with one or more blank spaces:"
grep ' ' document.txt

# 5. Select lines that contain digits and redirect to another file
echo -e "\nLines containing digits have been redirected to 'outputfile.txt':"
grep '[0-9]' document.txt > outputfile.txt

echo "The lines with digits have been saved in outputfile.txt"

