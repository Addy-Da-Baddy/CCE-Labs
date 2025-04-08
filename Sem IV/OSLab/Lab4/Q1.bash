#!/bin/bash
echo "Enter the name of the file to be duplicated: "
read file_name

if [ ! -f "$file_name" ]; then
  echo "Error: Fi;e $file_name does not exist"
  exit 1
fi

echo "Enter the number of copies to be made: "
read num_copies

if [ "$num_copies" -le 0 ]; then
  echo "Error: Number of copies must be a positive integer"
  exit 1
fi

for ((i=0; i<num_copies; i++)); do
    new_file_name="${file_name}_copy$((i+1))" # No spaces around '='
    cp "$file_name" "$new_file_name"
    echo "Created copy: $new_file_name"
done

