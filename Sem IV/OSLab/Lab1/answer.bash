#!/bin/bash

# Question 1: Create 10 files (log1.txt, log2.txt, ..., log10.txt) in ./sub1/sub2

mkdir -p ./sub1/sub2  
touch ./sub1/sub2/log{1..10}.txt  


# Question 2: Find all files in /var/log modified in the last 7 days


find /var/log -type f -mtime -7  

# Question 3: Rename all .txt files in the current directory to .dak files


for file in *.txt 
do
  mv "$file" "${file%.txt}.dak" 
done


