#include <stdio.h>

#define MAX 100

typedef struct Process {
    int id;
    int arrivalTime;
    int burstTime;
    int waitingTime;
    int turnaroundTime;
} Process;

void fcfs(Process p[], int n);
void display(Process p[], int n);

int main() {
    int n;
    Process processes[MAX];

    printf("Enter the number of processes: ");
    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        printf("Enter process ID, arrival time, and burst time: ");
        scanf("%d %d %d", &processes[i].id, &processes[i].arrivalTime, &processes[i].burstTime);
    }

    fcfs(processes, n);
    display(processes, n);

    return 0;
}

void fcfs(Process p[], int n) {
    int time = 0;
    
    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if (p[i].arrivalTime > p[j].arrivalTime) {
                Process temp = p[i];
                p[i] = p[j];
                p[j] = temp;
            }
        }
    }

    for (int i = 0; i < n; i++) {
        if (time < p[i].arrivalTime) {
            time = p[i].arrivalTime;
        }

        p[i].waitingTime = time - p[i].arrivalTime;
        
        p[i].turnaroundTime = p[i].waitingTime + p[i].burstTime;
        time += p[i].burstTime;
    }
}

void display(Process p[], int n) {
    printf("\nProcess ID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n");
    for (int i = 0; i < n; i++) {
        printf("%d\t\t%d\t\t%d\t\t%d\t\t%d\n", p[i].id, p[i].arrivalTime, p[i].burstTime, p[i].waitingTime, p[i].turnaroundTime);
    }
}
