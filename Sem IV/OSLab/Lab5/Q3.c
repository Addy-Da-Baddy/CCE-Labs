#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAX_STRINGS 100
#define MAX_LENGTH 100

void bubbleSort(char arr[][MAX_LENGTH], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (strcmp(arr[j], arr[j + 1]) > 0) {
                char temp[MAX_LENGTH];
                strcpy(temp, arr[j]);
                strcpy(arr[j], arr[j + 1]);
                strcpy(arr[j + 1], temp);
            }
        }
    }
}

void selectionSort(char arr[][MAX_LENGTH], int n) {
    for (int i = 0; i < n - 1; i++) {
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            if (strcmp(arr[j], arr[min_idx]) < 0) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            char temp[MAX_LENGTH];
            strcpy(temp, arr[i]);
            strcpy(arr[i], arr[min_idx]);
            strcpy(arr[min_idx], temp);
        }
    }
}

void printArray(char arr[][MAX_LENGTH], int n) {
    for (int i = 0; i < n; i++) {
        printf("%s\n", arr[i]);
    }
}

int main() {
    int N;

    printf("Enter the number of strings: ");
    scanf("%d", &N);

    char strings[N][MAX_LENGTH];
    printf("Enter the strings:\n");
    for (int i = 0; i < N; i++) {
        scanf("%s", strings[i]);
    }

    pid_t pid1, pid2;

    pid1 = fork();
    if (pid1 == 0) {
        printf("\nChild 1 (Bubble Sort) result:\n");
        bubbleSort(strings, N);
        printArray(strings, N);
        exit(0);
    }

    pid2 = fork();
    if (pid2 == 0) {
        printf("\nChild 2 (Selection Sort) result:\n");
        selectionSort(strings, N);
        printArray(strings, N);
        exit(0);
    }

    int status;
    waitpid(pid1, &status, 0);  
    waitpid(pid2, &status, 0); 

    printf("\nParent process: Both child processes are finished.\n");

    return 0;
}
