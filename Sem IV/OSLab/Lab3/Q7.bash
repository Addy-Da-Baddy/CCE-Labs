#!/bin/bash

# Ask user for the input file
echo "Enter the name of the file:"
read filename

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File not found!"
    exit 1
fi

# Create a temporary file to store the modified content
tempfile=$(mktemp)

# Loop through the file and keep only odd-numbered lines
awk 'NR % 2 != 0' "$filename" > "$tempfile"

# Replace the original file with the modified content
mv "$tempfile" "$filename"

echo "All even-numbered lines have been deleted from $filename."
