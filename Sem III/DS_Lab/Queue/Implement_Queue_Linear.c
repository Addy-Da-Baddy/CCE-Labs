#include <stdio.h>
#include <stdbool.h>

#define MAX_SIZE 15  // Correct the definition of MAX_SIZE

struct queue {
    int rear;
    int front;
    int arr[MAX_SIZE];
};

// Initialize the queue
void init(struct queue *q) {
    q->rear = -1;
    q->front = -1;  // Correct the initialization of front
    for (int i = 0; i < MAX_SIZE; i++) {
        q->arr[i] = 0;  // Correct the typo from srr to arr
    }
}

// Check if the queue is full
bool isFull(struct queue *q) {
    return (q->rear == MAX_SIZE - 1);
}

// Check if the queue is empty
bool isEmpty(struct queue *q) {
    return (q->rear == -1 && q->front == -1);
}

// Enqueue operation
void enq(struct queue *q, int num) {
    if (isFull(q)) {
        printf("Queue Overflow!\n");
        return;
    } else if (isEmpty(q)) {
        q->rear = q->front = 0;
    } else {
        q->rear++;
    }
    q->arr[q->rear] = num;
    return;
}

// Dequeue operation
int deque(struct queue *q) {
    if (isEmpty(q)) {  // Correct the syntax error for if condition
        printf("Queue Underflow!\n");
        return -1;  // Return a value to indicate queue underflow
    } else if (q->rear == q->front) {
        int x = q->arr[q->front];
        q->front = q->rear = -1;
        return x;  // Return the dequeued element
    } else {
        int x = q->arr[q->front];
        q->front++;
        return x;  // Return the dequeued element
    }
}

// Main function to demonstrate the queue operations
int main() {
    struct queue q;
    init(&q);

    enq(&q, 10);
    enq(&q, 20);
    enq(&q, 30);

    printf("Dequeued: %d\n", deque(&q));
    printf("Dequeued: %d\n", deque(&q));

    return 0;
}
