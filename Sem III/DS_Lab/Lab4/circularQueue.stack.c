#include <stdio.h>
#include <stdbool.h>

#define MAX 100

typedef struct Queue {
    int front;
    int rear;
    int items[MAX];
} Queue;

void init(Queue *q) {
    q->front = -1;
    q->rear = -1;
}

bool isFull(Queue *q) {
    return ((q->rear + 1) % MAX == q->front);
}

bool isEmpty(Queue *q) {
    return (q->front == -1);
}

void enq(Queue *q, int val) {
    if (isFull(q)) {
        printf("Queue overflow!\n");
    } else {
        if (isEmpty(q)) {
            q->front = 0;
        }
        q->rear = (q->rear + 1) % MAX;
        q->items[q->rear] = val;
        printf("Item Queued: %d\n", val);
    }
}

int deq(Queue *q) {
    if (isEmpty(q)) {
        printf("Queue underflow!\n");
        return -999999;
    } else {
        int val = q->items[q->front];
        if (q->front == q->rear) {
            init(q);
        } else {
            q->front = (q->front + 1) % MAX;
        }
        printf("Item dequeued: %d\n", val);
        return val;
    }
}

void display(Queue *q) {
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return;
    }
    printf("Queue: ");
    int i = q->front;
    while (true) {
        printf("%d ", q->items[i]);
        if (i == q->rear) break;
        i = (i + 1) % MAX;
    }
    printf("\n");
}

int main() {
    Queue q;
    init(&q);

    int choice, value;

    while (1) {
        printf("\nQueue Menu:\n");
        printf("1. Enqueue\n");
        printf("2. Dequeue\n");
        printf("3. Display\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to enqueue: ");
                scanf("%d", &value);
                enq(&q, value);
                break;

            case 2:
                deq(&q);
                break;

            case 3:
                display(&q);
                break;

            case 4:
                printf("Exiting...\n");
                return 0;

            default:
                printf("Invalid choice. Please enter a number between 1 and 4.\n");
                break;
        }
    }

    return 0;
}

