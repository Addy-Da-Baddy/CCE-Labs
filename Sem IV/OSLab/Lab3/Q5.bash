#!/bin/bash

# Prompt user for file extension and target folder
echo "Enter the file extension (e.g., .txt, .text):"
read file_extension

echo "Enter the target folder name (e.g., TEXT):"
read target_folder

# Check if target folder exists, if not, create it
if [ ! -d "$target_folder" ]; then
    mkdir "$target_folder"
    echo "Target folder '$target_folder' created."
fi

# Loop through all files in the current directory with the given extension
for file in *"$file_extension"; do
    if [ -f "$file" ]; then
        cp "$file" "$target_folder/"
        echo "Copied $file to $target_folder/"
    fi
done

echo "File copy operation completed."
