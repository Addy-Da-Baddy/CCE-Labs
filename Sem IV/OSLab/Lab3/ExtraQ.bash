#!/bin/bash

#Question: Display 5 largest files in both a directory and its subdirectories
#!/bin/bash

#!/bin/bash

# Prompt the user to enter a directory path using echo
echo "Enter the directory path to search: "
read DIR

# Check if the directory exists
if [ ! -d "$DIR" ]; then
  echo "The directory $DIR does not exist. Please try again."
  exit 1
fi

# Initialize an array to store file sizes and paths
file_sizes=()

# Use a for loop to iterate over each file in the directory and its subdirectories
for file in $(find "$DIR" -type f); do
  # Get the size of each file
  size=$(du -h "$file" | cut -f1)
  # Store the file size and file path
  file_sizes+=("$size $file")
done

# Sort the files by size in reverse order and display the top 5 largest files
echo "The 5 largest files are:"
echo "${file_sizes[@]}" | tr ' ' '\n' | sort -rh | head -n 5

