#include <stdio.h>
#include <stdlib.h>

// Define the Node structure
typedef struct Node {
    int data;
    struct Node* next;
} Node;

// Define the Queue structure
typedef struct Queue {
    Node* front;
    Node* rear;
    int size;
} Queue;

// Function to create a new node
Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

// Function to initialize a queue
void initQueue(Queue* queue) {
    queue->front = NULL;
    queue->rear = NULL;
    queue->size = 0;
}

// Function to enqueue an element into the queue
void enqueue(Queue* queue, int data) {
    Node* newNode = createNode(data);
    if (queue->rear == NULL) {
        // Queue is empty
        queue->front = newNode;
        queue->rear = newNode;
    } else {
        // Add to the end of the queue
        queue->rear->next = newNode;
        queue->rear = newNode;
    }
    queue->size++;
}

// Function to dequeue an element from the queue
int dequeue(Queue* queue) {
    if (queue->front == NULL) {
        printf("Queue underflow\n");
        exit(1);
    }
    Node* temp = queue->front;
    int data = temp->data;
    queue->front = queue->front->next;
    if (queue->front == NULL) {
        // Queue is now empty
        queue->rear = NULL;
    }
    free(temp);
    queue->size--;
    return data;
}

// Function to peek at the front element of the queue
int peek(const Queue* queue) {
    if (queue->front == NULL) {
        printf("Queue is empty\n");
        exit(1);
    }
    return queue->front->data;
}

// Function to print the queue
void printQueue(const Queue* queue) {
    Node* temp = queue->front;
    while (temp != NULL) {
        printf("%d", temp->data);
        temp = temp->next;
        if (temp != NULL) {
            printf(" -> ");
        }
    }
    printf("\n");
}

// Main function to test the queue implementation
int main() {
    Queue queue;
    initQueue(&queue);

    // Enqueue elements into the queue
    enqueue(&queue, 10);
    enqueue(&queue, 20);
    enqueue(&queue, 30);
    
    printf("Queue after enqueues:\n");
    printQueue(&queue);

    // Peek the front element
    printf("Front element: %d\n", peek(&queue));

    // Dequeue elements from the queue
    printf("Dequeued element: %d\n", dequeue(&queue));
    printf("Dequeued element: %d\n", dequeue(&queue));
    
    printf("Queue after dequeues:\n");
    printQueue(&queue);

    return 0;
}
