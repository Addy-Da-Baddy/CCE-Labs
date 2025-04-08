#include <stdio.h>

#define MAX 100

typedef struct Process {
    int id;
    int arrivalTime;
    int burstTime;
    int waitingTime;
    int turnaroundTime;
    int completed;
} Process;

void non_preemptive_sjf(Process p[], int n);
void display(Process p[], int n);

int main() {
    int n;
    Process processes[MAX];

    printf("Enter the number of processes: ");
    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        printf("Enter process ID, arrival time, and burst time: ");
        scanf("%d %d %d", &processes[i].id, &processes[i].arrivalTime, &processes[i].burstTime);
        processes[i].completed = 0;
    }

    non_preemptive_sjf(processes, n);
    display(processes, n);

    return 0;
}

void non_preemptive_sjf(Process p[], int n) {
    int time = 0, completed = 0, min_index;

    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if (p[i].arrivalTime > p[j].arrivalTime) {
                Process temp = p[i];
                p[i] = p[j];
                p[j] = temp;
            }
        }
    }

    while (completed != n) {
        min_index = -1;

        for (int i = 0; i < n; i++) {
            if (p[i].arrivalTime <= time && !p[i].completed) {
                if (min_index == -1 || p[i].burstTime < p[min_index].burstTime) {
                    min_index = i;
                }
            }
        }

        if (min_index != -1) {
            time += p[min_index].burstTime;
            p[min_index].completed = 1;
            completed++;

            p[min_index].turnaroundTime = time - p[min_index].arrivalTime;
            p[min_index].waitingTime = p[min_index].turnaroundTime - p[min_index].burstTime;
        } else {
            time++;
        }
    }
}

void display(Process p[], int n) {
    printf("Shortest Job First\n: " );
    printf("\nProcess ID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n");
    for (int i = 0; i < n; i++) {
        printf("%d\t\t%d\t\t%d\t\t%d\t\t%d\n", p[i].id, p[i].arrivalTime, p[i].burstTime, p[i].waitingTime, p[i].turnaroundTime);
    }
}
