#!/bin/bash

search_pattern() {
    input_file=$1
    echo "Searching for patterns in $input_file"
    for pattern in "${patterns[@]}"; do
        echo "Searching for pattern: $pattern"
        grep -n "$pattern" "$input_file"
    done
}

delete_pattern() {
    input_file=$1
    echo "Deleting patterns from $input_file"
    for pattern in "${patterns[@]}"; do
        echo "Deleting pattern: $pattern"
        sed -i "s/$pattern//g" "$input_file"
    done
}

menu() {
    input_file=$1
    while true; do
        echo "Select an operation:"
        echo "1. Search the patterns in the file"
        echo "2. Delete all occurrences of the patterns"
        echo "3. Exit"
        read -p "Enter your choice: " choice

        case $choice in
            1)
                search_pattern "$input_file"
                ;;
            2)
                delete_pattern "$input_file"
                ;;
            3)
                echo "Exiting the script."
                exit 0
                ;;
            *)
                echo "Invalid choice. Please try again."
                ;;
        esac
    done
}

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <input_file> <pattern1> [pattern2] ..."
    exit 1
fi

input_file=$1
shift
patterns=("$@")

if [ ! -f "$input_file" ]; then
    echo "Input file does not exist."
    exit 1
fi

menu "$input_file"
