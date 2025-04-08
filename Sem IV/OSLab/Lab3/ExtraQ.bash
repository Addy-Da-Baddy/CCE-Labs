#!/bin/bash

#Question: Display 5 largest files in both a directory and its subdirectories
#!/bin/bash

#!/bin/bash

# Prompt the user to enter a directory path using echo
echo "Enter the directory path to search: "
read DIR

if [ ! -d "$DIR" ]; then
  echo "The directory $DIR does not exist. Please try again."
  exit 1
fi

file_sizes=()

for file in $(find "$DIR" -type f); do
  size=$(du -h "$file" | cut -f1)
  file_sizes+=("$size $file")
done

echo "The 5 largest files are:"
echo "${file_sizes[@]}" | tr ' ' '\n' | sort -rh | head -n 5

