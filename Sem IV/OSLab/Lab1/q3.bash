#!/bin/bash

# 1. Find files with the .txt extension
echo "Files with .txt extension:"
find . -name "*.txt"
echo -e "\n--------------------------------------"

# 2. Find .txt files that contain at least one digit
echo "Files containing at least one digit:"
find -name "*[0-9]*"

echo -e "\n--------------------------------------"

# 3. Find .txt files that have a minimum length of 4 characters
echo "Files with .txt extension that have a minimum length of 4 characters:"
find -name "????*"



echo -e "\n--------------------------------------"

# 4. Find .txt files that do not start with a vowel
echo "Files with .txt extension that do not start with a vowel:"
find . -name '[^aeiouAEIOU]*'


