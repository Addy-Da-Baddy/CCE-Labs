#!/bin/bash

# Loop through all files in the current directory
for file in *; do
    # Check if it's a regular file
    if [ -f "$file" ]; then
        echo "Processing file: $file"
        sed -i -E 's/(^|\.[[:space:]])ex:/\1Example:/g' "$file"

        echo "Modifications done in $file"
    fi
done
