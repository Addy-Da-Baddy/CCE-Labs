#!/bin/bash

# Loop through all files in the current directory
for file in *; do
    # Check if it's a regular file
    if [ -f "$file" ]; then
        echo "Processing file: $file"
        
        # Use sed to modify lines where 'ex:' appears at the start of the line
        # or after a period followed by a space.
        sed -i -E 's/(^|\.[[:space:]])ex:/\1Example:/g' "$file"

        echo "Modifications done in $file"
    fi
done
