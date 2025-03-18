#include <stdio.h>
#include <stdbool.h>

#define MAX_PROCESSES 10
#define MAX_RESOURCES 10

int Allocation[MAX_PROCESSES][MAX_RESOURCES];
int Max[MAX_PROCESSES][MAX_RESOURCES];
int Need[MAX_PROCESSES][MAX_RESOURCES];
int Available[MAX_RESOURCES];

int n, m;  // Number of processes and resources

void calculateNeed() {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            Need[i][j] = Max[i][j] - Allocation[i][j];
        }
    }
}

// Function to check if a process can execute
bool canExecute(int process, int Work[]) {
    for (int j = 0; j < m; j++) {
        if (Need[process][j] > Work[j]) {
            return false;
        }
    }
    return true;
}

// Safety algorithm to check if the system is in a safe state
bool isSafe(int safeSequence[]) {
    int Work[MAX_RESOURCES];
    bool Finish[MAX_PROCESSES] = {false};
    
    for (int i = 0; i < m; i++) {
        Work[i] = Available[i];
    }

    int count = 0;
    while (count < n) {
        bool found = false;
        for (int i = 0; i < n; i++) {
            if (!Finish[i] && canExecute(i, Work)) {
                for (int j = 0; j < m; j++) {
                    Work[j] += Allocation[i][j];
                }
                safeSequence[count++] = i;
                Finish[i] = true;
                found = true;
            }
        }
        if (!found) {
            return false;  // No safe sequence found, system is in deadlock
        }
    }
    return true;
}

// Resource request algorithm
bool requestResources(int process, int request[]) {
    // Check if request exceeds Need
    for (int i = 0; i < m; i++) {
        if (request[i] > Need[process][i]) {
            printf("Error: Process %d requested more than its maximum need!\n", process);
            return false;
        }
    }

    // Check if request exceeds Available resources
    for (int i = 0; i < m; i++) {
        if (request[i] > Available[i]) {
            printf("Process %d must wait, insufficient resources.\n", process);
            return false;
        }
    }

    // Pretend allocation (temporary allocation for safety check)
    for (int i = 0; i < m; i++) {
        Available[i] -= request[i];
        Allocation[process][i] += request[i];
        Need[process][i] -= request[i];
    }

    // Check if system remains in a safe state
    int safeSequence[MAX_PROCESSES];
    if (isSafe(safeSequence)) {
        printf("Request granted. System remains in safe state.\n");
        return true;
    } else {
        // Rollback allocation
        printf("Request denied. System would enter an unsafe state!\n");
        for (int i = 0; i < m; i++) {
            Available[i] += request[i];
            Allocation[process][i] -= request[i];
            Need[process][i] += request[i];
        }
        return false;
    }
}

int main() {
    printf("Enter number of processes: ");
    scanf("%d", &n);
    printf("Enter number of resource types: ");
    scanf("%d", &m);

    printf("Enter Allocation Matrix:\n");
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &Allocation[i][j]);

    printf("Enter Max Matrix:\n");
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &Max[i][j]);

    printf("Enter Available Resources:\n");
    for (int i = 0; i < m; i++)
        scanf("%d", &Available[i]);

    // Calculate Need Matrix
    calculateNeed();

    // Check if system is in a safe state
    int safeSequence[MAX_PROCESSES];
    if (isSafe(safeSequence)) {
        printf("System is in a SAFE state. Safe sequence: ");
        for (int i = 0; i < n; i++) {
            printf("P%d ", safeSequence[i]);
        }
        printf("\n");
    } else {
        printf("System is in DEADLOCK!\n");
    }

    // Simulating a resource request
    int process;
    int request[MAX_RESOURCES];
    
    printf("Enter process number making a request: ");
    scanf("%d", &process);
    printf("Enter resource request vector:\n");
    for (int i = 0; i < m; i++)
        scanf("%d", &request[i]);

    requestResources(process, request);

    return 0;
}
