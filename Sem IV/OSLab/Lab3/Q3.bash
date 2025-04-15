#!/bin/bash
echo "Enter the directory path to search: "
read DIR

if [ ! -d "$DIR" ]; then
  echo "The directory $DIR does not exist."
  exit 1
fi

echo "The 5 largest files are:"
for file in $(find "$DIR" -type f); do
  size=$(du -h "$file" | cut -f1)
  echo "$size $file"
done | sort -rh | head -n 5

#!/bin/bash

for file in $(find . -type f -name "*.txt"); do
    newfile="${file%.txt}.text"
    
    mv "$file" "$newfile"
    
    echo "Renamed $file to $newfile"
done
