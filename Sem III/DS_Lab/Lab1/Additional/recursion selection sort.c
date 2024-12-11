#include <stdio.h>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void recursiveSelectionSort(int arr[], int start, int n) {
    if (start >= n - 1) {
        return;
    }

    int minIndex = start;
    for (int i = start + 1; i < n; i++) {
        if (arr[i] < arr[minIndex]) {
            minIndex = i;
        }
    }

    swap(&arr[start], &arr[minIndex]);

    recursiveSelectionSort(arr, start + 1, n);
}

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int arr[] = {64, 25, 12, 22, 11};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Original array:\n");
    printArray(arr, n);

    recursiveSelectionSort(arr, 0, n);

    printf("Sorted array:\n");
    printArray(arr, n);

    return 0;
}
