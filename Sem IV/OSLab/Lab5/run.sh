 #!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: $0 <source_file.c>"
    exit 1
fi

SOURCE_FILE=$1

if [ ! -f "$SOURCE_FILE" ]; then
    echo "File '$SOURCE_FILE' not found!"
    exit 1
fi

EXEC_NAME="exec"

gcc -o "$EXEC_NAME" "$SOURCE_FILE"

if [ $? -eq 0 ]; then
    chmod +x "$EXEC_NAME"
    
    ./"$EXEC_NAME"
else
    echo "Compilation failed!"
    exit 1
 fi
 
