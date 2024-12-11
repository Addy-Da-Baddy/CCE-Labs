#include <stdio.h>
#include <stdbool.h>

#define MAX_SIZE 5

struct queue {
    int rear;
    int front;
    int arr[MAX_SIZE];
};

// Initialize the queue
void init(struct queue *q) {
    q->rear = -1;
    q->front = -1;
    for (int i = 0; i < MAX_SIZE; i++) {
        q->arr[i] = 0;
    }
}

// Check if the queue is full
bool isFull(struct queue *q) {
    return ((q->rear + 1) % MAX_SIZE == q->front);
}

// Check if the queue is empty
bool isEmpty(struct queue *q) {
    return (q->front == -1 && q->rear == -1);
}

// Enqueue operation
void enq(struct queue *q, int num) {
    if (isFull(q)) {
        printf("Queue Overflow!\n");
        return;
    }
    if (isEmpty(q)) {
        q->front = q->rear = 0;
    } else {
        q->rear = (q->rear + 1) % MAX_SIZE;
    }
    q->arr[q->rear] = num;
    printf("Enqueued: %d\n", num);
}

// Dequeue operation
int deq(struct queue *q) {
    if (isEmpty(q)) {
        printf("Queue Underflow!\n");
        return -1;
    }
    int x = q->arr[q->front];
    if (q->front == q->rear) {
        // Last element being removed
        q->front = q->rear = -1;
    } else {
        q->front = (q->front + 1) % MAX_SIZE;
    }
    return x;
}

// Display the queue
void display(struct queue *q) {
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return;
    }
    printf("Queue: ");
    int i = q->front;
    do {
        printf("%d ", q->arr[i]);
        i = (i + 1) % MAX_SIZE;
    } while (i != (q->rear + 1) % MAX_SIZE);
    printf("\n");
}

// Main function to demonstrate the circular queue operations
int main() {
    struct queue q;
    init(&q);

    enq(&q, 10);
    enq(&q, 20);
    enq(&q, 30);
    display(&q);

    printf("Dequeued: %d\n", deq(&q));
    display(&q);

    enq(&q, 40);
    enq(&q, 50);
    display(&q);

    enq(&q, 60);  // This should print "Queue Overflow!"

    printf("Dequeued: %d\n", deq(&q));
    enq(&q, 60);
    display(&q);

    return 0;
}