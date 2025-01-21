#!/bin/bash

echo "Enter your base salary"
read base_salary

echo "Enter your travel allowance (TA)"
read TA

bonus=$(echo "$base_salary * 0.10" | bc)

total_salary=$(echo "$base_salary + $TA + $bonus" | bc)

echo "Your total salary is $total_salary"
