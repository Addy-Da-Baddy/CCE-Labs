#include <stdio.h>
#include <stdlib.h>

#define MAX 100  // Maximum size of the heap

// Define a heap structure
typedef struct {
    int arr[MAX];
    int size;
} Heap;

// Function prototypes
void initHeap(Heap* heap);
void insertMax(Heap* heap, int val);
void delMax(Heap* heap);
void heapify(int arr[], int n, int i);
void swap(int* a, int* b);
void printHeap(Heap* heap);

// Initialize the heap
void initHeap(Heap* heap) {
    heap->size = 0;
    heap->arr[0] = -1;  // Not using index 0 (1-based index)
}

// Insert an element into the max-heap
void insertMax(Heap* heap, int val) {
    heap->size++;
    int index = heap->size;   // Insert at the end
    heap->arr[index] = val;

    // Propagate the new element upwards to maintain the max-heap property
    while (index > 1) {
        int parent = index / 2;
        if (heap->arr[parent] < heap->arr[index]) {
            swap(&heap->arr[parent], &heap->arr[index]);
            index = parent;
        } else {
            break;
        }
    }
}

/*
To convert insertMax into insertMin (for a min-heap):
- Change the condition in the `while` loop to: heap->arr[parent] > heap->arr[index]
- This will ensure that the smallest element is at the root (min-heap property).
*/

// Delete the maximum element (root) from the max-heap
void delMax(Heap* heap) {
    if (heap->size == 0) {
        printf("Heap is empty\n");
        return;
    }

    // Replace root with the last element in the heap
    heap->arr[1] = heap->arr[heap->size];
    heap->size--;  // Reduce heap size

    // Reheapify the root to maintain the max-heap property
    heapify(heap->arr, heap->size, 1);
}

/*
To convert delMax into delMin (for a min-heap):
- Use the same structure but heapify the array using a modified min-heapify function,
  which ensures the smallest element stays at the root.
*/

// Heapify function to maintain the max-heap property
void heapify(int arr[], int n, int i) {
    int largest = i;           // Initialize largest as root
    int leftChild = 2 * i;      // Left child index
    int rightChild = 2 * i + 1; // Right child index

    // If the left child is larger than the root
    if (leftChild <= n && arr[leftChild] > arr[largest]) {
        largest = leftChild;
    }

    // If the right child is larger than the current largest
    if (rightChild <= n && arr[rightChild] > arr[largest]) {
        largest = rightChild;
    }

    // If the largest is not the root
    if (largest != i) {
        // Swap root with the largest child
        swap(&arr[i], &arr[largest]);

        // Recursively heapify the affected subtree
        heapify(arr, n, largest);
    }
}

/*
To convert heapify into min-heapify (for a min-heap):
- Change the comparisons in the `if` conditions:
  arr[leftChild] < arr[i] and arr[rightChild] < arr[largest]
  This will maintain the min-heap property, ensuring the smallest element is at the root.
*/






// Utility function to swap two elements
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Print the heap
void printHeap(Heap* heap) {
    printf("Heap elements: ");
    for (int i = 1; i <= heap->size; i++) {
        printf("%d ", heap->arr[i]);
    }
    printf("\n");
}

// Main function to demonstrate the max-heap operations
int main() {
    Heap maxHeap;
    initHeap(&maxHeap);

    // Inserting elements into the max-heap
    insertMax(&maxHeap, 10);
    insertMax(&maxHeap, 20);
    insertMax(&maxHeap, 15);
    insertMax(&maxHeap, 30);
    insertMax(&maxHeap, 25);

    // Print heap
    printHeap(&maxHeap);  // Output: 30 25 15 10 20

    // Delete the max element (root)
    delMax(&maxHeap);
    printHeap(&maxHeap);  // Output: 25 20 15 10

    return 0;
}
