#!/bin/bash

file_list=()

while true; do
    read -p "Enter the name of the file to add to the list (or press Enter to proceed to deletion): " file_name
    
    if [ -z "$file_name" ]; then
        echo "Proceeding to deletion..."
        break
    fi
    
    if [ -f "$file_name" ]; then
        file_list+=("$file_name")
        echo "$file_name has been added to the list."
    else
        echo "Error: File '$file_name' does not exist. It will not be added to the list."
    fi
    
    read -p "Do you want to add another file? (Yes/No): " add_more
    if [[ "$add_more" == "No" || "$add_more" == "no" ]]; then
        echo "Proceeding to deletion..."
        break
    fi
done

read -p "Are you sure you want to permanently delete all the files in the list? This cannot be undone. Enter '0' to cancel, or any other key to confirm: " confirm_delete

if [ "$confirm_delete" -eq 0 ]; then
    echo "Deletion canceled. No files have been deleted."
else
    for filename in "${file_list[@]}"; do
        rm "$filename"  
        echo "$filename has been permanently deleted."
    done

    echo "All files in the list have been deleted."
fi

echo "Script execution complete."
