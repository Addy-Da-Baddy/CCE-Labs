#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX 100

typedef struct Process {
    int id;
    int priority;
    int arrivalTime;
    int burstTime;
    int remainingTime;
    int turnaroundTime;
    int waitingTime;
    bool completed;
} Process;

void preemptive_sjf(Process p[], int n);
void round_robin(Process p[], int n, int quantum);
void non_preemptive_priority(Process p[], int n);

void display(Process p[], int n) {
    printf("\nProcess ID\tBurst Time\tArrival Time\tPriority\tWaiting Time\tTurnaround Time\n");
    for (int i = 0; i < n; i++) {
        printf("%d\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\n", p[i].id, p[i].burstTime, p[i].arrivalTime, p[i].priority, p[i].waitingTime, p[i].turnaroundTime);
    }
}

int main() {
    int n, choice, quantum;
    Process processes[MAX];

    printf("Enter the number of processes: ");
    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        printf("Enter process ID, priority, arrival time, burst time: ");
        scanf("%d %d %d %d", &processes[i].id, &processes[i].priority, &processes[i].arrivalTime, &processes[i].burstTime);
        processes[i].remainingTime = processes[i].burstTime;
        processes[i].completed = false;
    }

    do {
        printf("\nMenu:\n");
        printf("1. Preemptive SJF\n");
        printf("2. Round Robin\n");
        printf("3. Non-Preemptive Priority Scheduling\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                preemptive_sjf(processes, n);
                break;
            case 2:
                printf("Enter time quantum: ");
                scanf("%d", &quantum);
                round_robin(processes, n, quantum);
                break;
            case 3:
                non_preemptive_priority(processes, n);
                break;
            case 4:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice! Try again.\n");
        }
    } while (choice != 4);

    return 0;
}



void preemptive_sjf(Process p[], int n) {
    int time = 0, completed = 0, min_index;
    while (completed != n) {
        min_index = -1;
        for (int i = 0; i < n; i++) {
            if (p[i].arrivalTime <= time && !p[i].completed) {
                if (min_index == -1 || p[i].remainingTime < p[min_index].remainingTime) {
                    min_index = i;
                }
            }
        }

        if (min_index != -1) {
            p[min_index].remainingTime--;
            if (p[min_index].remainingTime == 0) {
                p[min_index].completed = true;
                completed++;
                p[min_index].turnaroundTime = time + 1 - p[min_index].arrivalTime;
                p[min_index].waitingTime = p[min_index].turnaroundTime - p[min_index].burstTime;
            }
            time++;
        } else {
            time++;
        }
    }
    display(p, n);
}

void round_robin(Process p[], int n, int quantum) {
    int time = 0, completed = 0;
    int remainingProcesses = n;

    for (int i = 0; i < n; i++) {
        p[i].remainingTime = p[i].burstTime;
        p[i].completed = false;
    }

    while (completed != n) {
        for (int i = 0; i < n; i++) {
            if (p[i].arrivalTime <= time && !p[i].completed) {
                if (p[i].remainingTime > quantum) {
                    p[i].remainingTime -= quantum;
                    time += quantum;
                } else {
                    time += p[i].remainingTime;
                    p[i].remainingTime = 0;
                    p[i].completed = true;
                    completed++;
                    p[i].turnaroundTime = time - p[i].arrivalTime;
                    p[i].waitingTime = p[i].turnaroundTime - p[i].burstTime;
                }
            }
        }
    }
    display(p, n);
}

void non_preemptive_priority(Process p[], int n) {
    int time = 0, completed = 0, selected_index = -1;
    while (completed != n) {
        selected_index = -1;
        bool process_selected = false;

        for (int i = 0; i < n; i++) {
            if (p[i].arrivalTime <= time && !p[i].completed) {
                if (selected_index == -1 || p[i].priority < p[selected_index].priority ||
                    (p[i].priority == p[selected_index].priority && p[i].arrivalTime < p[selected_index].arrivalTime)) {
                    selected_index = i;
                    process_selected = true;
                }
            }
        }

        if (process_selected) {
            time += p[selected_index].burstTime;
            p[selected_index].completed = true;
            completed++;
            p[selected_index].turnaroundTime = time - p[selected_index].arrivalTime;
            p[selected_index].waitingTime = p[selected_index].turnaroundTime - p[selected_index].burstTime;
        } else {
            time++;
        }
    }
    display(p, n);
}
