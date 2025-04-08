#!/bin/bash
echo "Enter the name of the directory"
read dirname

if [ ! -d "$dirname" ]; then
    echo "Directory does not exist"
    exit 1
fi

echo "Enter the pattern of filename to search for"
read pattern

ans=$(find "$dirname" -type f -name "$pattern")

echo "$ans"
