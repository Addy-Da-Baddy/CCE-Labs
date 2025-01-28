
#!/bin/bash

# Bubble Sort function
bubble_sort() {


    local n=$#
    local arr=("$@")

    # Bubble Sort algorithm
    for ((i = 0; i < n; i++)); do
        for ((j = 0; j < n - 1 - i; j++)); do
            # Compare adjacent elements and swap if they are in the wrong order
            if [[ "${arr[j]}" > "${arr[j+1]}" ]]; then
                # Swap elements
                temp="${arr[j]}"
                arr[j]="${arr[j+1]}"
                arr[j+1]="$temp"
            fi
        done
    done
    
    for word in "${arr[@]}"; do
        echo "$word"
    done
}

bubble_sort "$@"
