#!/bin/bash

for file in $(find . -type f -name "*.txt"); do
    newfile="${file%.txt}.text"
    
    mv "$file" "$newfile"
    
    echo "Renamed $file to $newfile"
done
