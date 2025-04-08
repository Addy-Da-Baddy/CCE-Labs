#include <stdio.h>
#include <stdbool.h>

#define MAX_PROCESSES 5
#define MAX_RESOURCES 3

// Function to calculate the 'Need' matrix
void calculateNeed(int need[MAX_PROCESSES][MAX_RESOURCES], int max[MAX_PROCESSES][MAX_RESOURCES], int allot[MAX_PROCESSES][MAX_RESOURCES], int num_processes, int num_resources) {
    for (int i = 0; i < num_processes; i++)
        for (int j = 0; j < num_resources; j++)
            need[i][j] = max[i][j] - allot[i][j];
}

// Function to simulate Banker's Algorithm and check if the system is in a safe state
bool BankersAlgo(int avail[], int max[][MAX_RESOURCES], int allot[][MAX_RESOURCES], int num_processes, int num_resources) {
    int need[MAX_PROCESSES][MAX_RESOURCES];
    calculateNeed(need, max, allot, num_processes, num_resources);

    bool finish[MAX_PROCESSES] = {0}; // To track if a process has finished
    int safeSequence[MAX_PROCESSES];  // To store the safe sequence
    int work[MAX_RESOURCES];

    for (int i = 0; i < num_resources; i++) {
        work[i] = avail[i];  // Initialize work array with available resources
    }

    int count = 0; // To count the number of processes that can finish
    while (count < num_processes) {
        bool found = false;
        for (int p = 0; p < num_processes; p++) {
            if (!finish[p]) {
                int j;
                // Check if the process can be completed with the available resources
                for (j = 0; j < num_resources; j++) {
                    if (need[p][j] > work[j]) {
                        break;
                    }
                }

                if (j == num_resources) {
                    // Process can be completed
                    for (int k = 0; k < num_resources; k++) {
                        work[k] += allot[p][k];  // Release the resources allocated to this process
                    }

                    safeSequence[count++] = p;  // Add the process to the safe sequence
                    finish[p] = 1;  // Mark process as finished
                    found = true;
                    break; // Proceed to check the next process
                }
            }
        }

        if (!found) {
            // If no process can be finished, the system is in a deadlock state
            printf("System is not in a safe state, deadlocked.\n");
            return false;
        }
    }

    // If the loop completes successfully, the system is in a safe state
    printf("System is in a safe state\nSafe sequence is: ");
    for (int i = 0; i < count; i++) {
        printf("%d ", safeSequence[i]);
    }
    printf("\n");

    return true;
}

// Function to handle resource requests
bool requestResources(int process_id, int request[], int avail[], int max[][MAX_RESOURCES], int allot[][MAX_RESOURCES], int num_processes, int num_resources) {
    int need[MAX_PROCESSES][MAX_RESOURCES];
    calculateNeed(need, max, allot, num_processes, num_resources);

    // Check if request is less than need
    for (int j = 0; j < num_resources; j++) {
        if (request[j] > need[process_id][j]) {
            printf("Error: Process has exceeded its maximum claim.\n");
            return false;
        }
    }

    // Check if request is less than available resources
    for (int j = 0; j < num_resources; j++) {
        if (request[j] > avail[j]) {
            printf("Resources are not available.\n");
            return false;
        }
    }

    // Pretend to allocate requested resources
    for (int j = 0; j < num_resources; j++) {
        avail[j] -= request[j];
        allot[process_id][j] += request[j];
        need[process_id][j] -= request[j];
    }

    // Check if the new state is safe
    if (BankersAlgo(avail, max, allot, num_processes, num_resources)) {
        printf("Request can be granted.\n");
        return true;
    } else {
        // Rollback if not safe
        for (int j = 0; j < num_resources; j++) {
            avail[j] += request[j];
            allot[process_id][j] -= request[j];
            need[process_id][j] += request[j];
        }
        printf("Request cannot be granted as it leads to an unsafe state.\n");
        return false;
    }
}

int main() {
    printf("BankersAlgo\n");
    int num_processes, num_resources;
    printf("Enter number of processes: ");
    scanf("%d", &num_processes);
    printf("Enter number of resources: ");
    scanf("%d", &num_resources);

    int avail[MAX_RESOURCES];  // Available resources
    printf("Enter available resources: ");
    for (int i = 0; i < num_resources; i++) {
        scanf("%d", &avail[i]);
    }

    int max[MAX_PROCESSES][MAX_RESOURCES];  // Maximum resources needed by each process
    printf("Enter maximum resources for each process:\n");
    for (int i = 0; i < num_processes; i++) {
        for (int j = 0; j < num_resources; j++) {
            scanf("%d", &max[i][j]);
        }
    }

    int allot[MAX_PROCESSES][MAX_RESOURCES];  // Allocated resources for each process
    printf("Enter allocated resources for each process:\n");
    for (int i = 0; i < num_processes; i++) {
        for (int j = 0; j < num_resources; j++) {
            scanf("%d", &allot[i][j]);
        }
    }

    BankersAlgo(avail, max, allot, num_processes, num_resources);

    // Example resource request
    int process_id, request[MAX_RESOURCES];
    printf("Enter process ID for resource request: ");
    scanf("%d", &process_id);
    printf("Enter resource request: ");
    for (int i = 0; i < num_resources; i++) {
        scanf("%d", &request[i]);
    }

    requestResources(process_id, request, avail, max, allot, num_processes, num_resources);

    return 0;
}