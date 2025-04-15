#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int id;
    int period;
    int execution_time;
    int deadline;
    int remaining_time;
} Task;

void rateMonotonic(Task tasks[], int n) {
    printf("\nRate-Monotonic Scheduling:\n");
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (tasks[i].period > tasks[j].period) {
                Task temp = tasks[i];
                tasks[i] = tasks[j];
                tasks[j] = temp;
            }
        }
    }

    for (int time = 0; time < 10; ++time) {
        for (int i = 0; i < n; ++i) {
            if (tasks[i].remaining_time > 0) {
                printf("Time %d: Executing Task %d\n", time, tasks[i].id);
                --tasks[i].remaining_time;
                break;
            }
        }
    }
}

void earliestDeadlineFirst(Task tasks[], int n) {
    printf("\nEarliest-Deadline-First Scheduling:\n");
    for (int time = 0; time < 10; ++time) {
        int min_deadline_idx = -1;
        for (int i = 0; i < n; ++i) {
            if (tasks[i].remaining_time > 0 &&
                (min_deadline_idx == -1 || tasks[i].deadline < tasks[min_deadline_idx].deadline)) {
                min_deadline_idx = i;
            }
        }

        if (min_deadline_idx != -1) {
            printf("Time %d: Executing Task %d\n", time, tasks[min_deadline_idx].id);
            --tasks[min_deadline_idx].remaining_time;
            tasks[min_deadline_idx].deadline--;
        }
    }
}

int main() {
    int n;

    printf("Enter the number of tasks: ");
    scanf("%d", &n);

    Task tasks[n];

    for (int i = 0; i < n; ++i) {
        printf("\nEnter details for Task %d:\n", i + 1);
        tasks[i].id = i + 1;
        printf("Period: ");
        scanf("%d", &tasks[i].period);
        printf("Execution Time: ");
        scanf("%d", &tasks[i].execution_time);
        tasks[i].deadline = tasks[i].period; 
        tasks[i].remaining_time = tasks[i].execution_time;
    }

    rateMonotonic(tasks, n);

    // Reset remaining times for EDF simulation
    for (int i = 0; i < n; ++i) {
        tasks[i].remaining_time = tasks[i].execution_time;
        tasks[i].deadline = tasks[i].period;
    }

    earliestDeadlineFirst(tasks, n);

    return 0;
}




// With arrival time cuz ajith ro raha tha

#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int id;
    int period;
    int execution_time;
    int deadline;
    int remaining_time;
    int arrival_time; // Arrival time added
} Task;

// Rate-Monotonic Scheduling (RMS)
void rateMonotonic(Task tasks[], int n) {
    printf("\nRate-Monotonic Scheduling:\n");

    // Sort tasks by period (shorter periods have higher priority)
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (tasks[i].period > tasks[j].period) {
                Task temp = tasks[i];
                tasks[i] = tasks[j];
                tasks[j] = temp;
            }
        }
    }

    for (int time = 0; time < 10; ++time) {
        // Find the first task that has arrived and has remaining time
        for (int i = 0; i < n; ++i) {
            if (tasks[i].arrival_time <= time && tasks[i].remaining_time > 0) {
                printf("Time %d: Executing Task %d\n", time, tasks[i].id);
                --tasks[i].remaining_time;
                break;
            }
        }
    }
}

// Earliest Deadline First (EDF) Scheduling
void earliestDeadlineFirst(Task tasks[], int n) {
    printf("\nEarliest-Deadline-First Scheduling:\n");

    for (int time = 0; time < 10; ++time) {
        int min_deadline_idx = -1;

        // Find the task with the earliest deadline and that has arrived
        for (int i = 0; i < n; ++i) {
            if (tasks[i].arrival_time <= time && tasks[i].remaining_time > 0 &&
                (min_deadline_idx == -1 || tasks[i].deadline < tasks[min_deadline_idx].deadline)) {
                min_deadline_idx = i;
            }
        }

        if (min_deadline_idx != -1) {
            printf("Time %d: Executing Task %d\n", time, tasks[min_deadline_idx].id);
            --tasks[min_deadline_idx].remaining_time;
            tasks[min_deadline_idx].deadline--; // Update deadline after execution
        }
    }
}

int main() {
    int n;

    printf("Enter the number of tasks: ");
    scanf("%d", &n);

    Task tasks[n];

    // Input task details
    for (int i = 0; i < n; ++i) {
        printf("\nEnter details for Task %d:\n", i + 1);
        tasks[i].id = i + 1;
        printf("Period: ");
        scanf("%d", &tasks[i].period);
        printf("Execution Time: ");
        scanf("%d", &tasks[i].execution_time);
        printf("Arrival Time: ");
        scanf("%d", &tasks[i].arrival_time);

        tasks[i].deadline = tasks[i].period; 
        tasks[i].remaining_time = tasks[i].execution_time;
    }

    // Run Rate-Monotonic Scheduling
    rateMonotonic(tasks, n);

    // Reset tasks for EDF
    for (int i = 0; i < n; ++i) {
        tasks[i].remaining_time = tasks[i].execution_time;
        tasks[i].deadline = tasks[i].period;
    }

    // Run Earliest-Deadline-First Scheduling
    earliestDeadlineFirst(tasks, n);

    return 0;
}

