#include <stdio.h>
#include <stdlib.h>

#define MAX 100

void fcfs(int requests[], int n, int head) {
    int total_head_movement = 0;
    printf("\nFCFS Disk Scheduling\nOrder of execution: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", requests[i]);
        total_head_movement += abs(requests[i] - head);
        head = requests[i];
    }
    printf("\nTotal head movement: %d\n", total_head_movement);
}

void sstf(int requests[], int n, int head) {
    int total_head_movement = 0, visited[MAX] = {0}, count = 0;
    printf("\nSSTF Disk Scheduling\nOrder of execution: ");

    while (count < n) {
        int min_distance = 1e9, index = -1;
        for (int i = 0; i < n; i++) {
            if (!visited[i] && abs(requests[i] - head) < min_distance) {
                min_distance = abs(requests[i] - head);
                index = i;
            }
        }
        visited[index] = 1;
        printf("%d ", requests[index]);
        total_head_movement += min_distance;
        head = requests[index];
        count++;
    }
    printf("\nTotal head movement: %d\n", total_head_movement);
}

void scan(int requests[], int n, int head, int disk_size) {
    int total_head_movement = 0, i;
    int left[MAX], right[MAX], lcount = 0, rcount = 0;

    for (i = 0; i < n; i++) {
        if (requests[i] < head)
            left[lcount++] = requests[i];
        else
            right[rcount++] = requests[i];
    }

    left[lcount++] = 0; // Include 0
    qsort(left, lcount, sizeof(int), (int (*)(const void *, const void *))abs);
    qsort(right, rcount, sizeof(int), (int (*)(const void *, const void *))abs);

    printf("\nSCAN Disk Scheduling\nOrder of execution: ");
    for (i = 0; i < rcount; i++) {
        printf("%d ", right[i]);
        total_head_movement += abs(right[i] - head);
        head = right[i];
    }
    for (i = lcount - 1; i >= 0; i--) {
        printf("%d ", left[i]);
        total_head_movement += abs(left[i] - head);
        head = left[i];
    }
    printf("\nTotal head movement: %d\n", total_head_movement);
}

void c_scan(int requests[], int n, int head, int disk_size) {
    int total_head_movement = 0, i;
    int left[MAX], right[MAX], lcount = 0, rcount = 0;

    for (i = 0; i < n; i++) {
        if (requests[i] < head)
            left[lcount++] = requests[i];
        else
            right[rcount++] = requests[i];
    }

    left[lcount++] = 0; // Start at 0
    right[rcount++] = disk_size - 1; // End at max

    qsort(left, lcount, sizeof(int), (int (*)(const void *, const void *))abs);
    qsort(right, rcount, sizeof(int), (int (*)(const void *, const void *))abs);

    printf("\nC-SCAN Disk Scheduling\nOrder of execution: ");
    for (i = 0; i < rcount; i++) {
        printf("%d ", right[i]);
        total_head_movement += abs(right[i] - head);
        head = right[i];
    }
    head = 0;
    for (i = 0; i < lcount; i++) {
        printf("%d ", left[i]);
        total_head_movement += abs(left[i] - head);
        head = left[i];
    }
    printf("\nTotal head movement: %d\n", total_head_movement);
}

void look(int requests[], int n, int head) {
    int total_head_movement = 0, i;
    int left[MAX], right[MAX], lcount = 0, rcount = 0;

    for (i = 0; i < n; i++) {
        if (requests[i] < head)
            left[lcount++] = requests[i];
        else
            right[rcount++] = requests[i];
    }

    qsort(left, lcount, sizeof(int), (int (*)(const void *, const void *))abs);
    qsort(right, rcount, sizeof(int), (int (*)(const void *, const void *))abs);

    printf("\nLOOK Disk Scheduling\nOrder of execution: ");
    for (i = 0; i < rcount; i++) {
        printf("%d ", right[i]);
        total_head_movement += abs(right[i] - head);
        head = right[i];
    }
    for (i = lcount - 1; i >= 0; i--) {
        printf("%d ", left[i]);
        total_head_movement += abs(left[i] - head);
        head = left[i];
    }
    printf("\nTotal head movement: %d\n", total_head_movement);
}

void c_look(int requests[], int n, int head) {
    int total_head_movement = 0, i;
    int left[MAX], right[MAX], lcount = 0, rcount = 0;

    for (i = 0; i < n; i++) {
        if (requests[i] < head)
            left[lcount++] = requests[i];
        else
            right[rcount++] = requests[i];
    }

    qsort(left, lcount, sizeof(int), (int (*)(const void *, const void *))abs);
    qsort(right, rcount, sizeof(int), (int (*)(const void *, const void *))abs);

    printf("\nC-LOOK Disk Scheduling\nOrder of execution: ");
    for (i = 0; i < rcount; i++) {
        printf("%d ", right[i]);
        total_head_movement += abs(right[i] - head);
        head = right[i];
    }
    for (i = 0; i < lcount; i++) {
        printf("%d ", left[i]);
        total_head_movement += abs(left[i] - head);
        head = left[i];
    }
    printf("\nTotal head movement: %d\n", total_head_movement);
}

int main() {
    int n, head, choice, disk_size;
    int requests[MAX];

    printf("Enter the number of requests: ");
    scanf("%d", &n);
    printf("Enter the request queue: ");
    for (int i = 0; i < n; i++)
        scanf("%d", &requests[i]);
    printf("Enter initial head position: ");
    scanf("%d", &head);
    printf("Enter disk size: ");
    scanf("%d", &disk_size);

    while (1) {
        printf("\nDisk Scheduling Algorithms:\n");
        printf("1. FCFS\n2. SSTF\n3. SCAN\n4. C-SCAN\n5. LOOK\n6. C-LOOK\n7. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: fcfs(requests, n, head); break;
            case 2: sstf(requests, n, head); break;
            case 3: scan(requests, n, head, disk_size); break;
            case 4: c_scan(requests, n, head, disk_size); break;
            case 5: look(requests, n, head); break;
            case 6: c_look(requests, n, head); break;
            case 7: exit(0);
            default: printf("Invalid choice!\n");
        }
    }
    return 0;
}
