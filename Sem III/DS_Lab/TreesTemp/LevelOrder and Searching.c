#include <stdio.h>
#include <stdlib.h>

#define MAXSIZE 100

typedef struct Node {
    int data;
    struct Node* llink;
    struct Node* rlink;
} Node;

// Queue structure for storing nodes
typedef struct {
    Node* items[MAXSIZE];
    int front, rear;
} Queue;

// Function to initialize the queue
void initializeQueue(Queue* queue) {
    queue->front = queue->rear = -1;
}

// Function to check if the queue is empty
int isEmpty(Queue* queue) {
    return queue->front == -1;
}

// Function to enqueue a node
void enqueue(Queue* queue, Node* node) {
    if (queue->rear == MAXSIZE - 1) {
        printf("Queue overflow\n");
        return;
    }
    if (queue->front == -1) queue->front = 0;
    queue->items[++queue->rear] = node;
}

// Function to dequeue a node
Node* dequeue(Queue* queue) {
    if (isEmpty(queue)) {
        return NULL;
    }
    Node* node = queue->items[queue->front];
    if (queue->front == queue->rear) {
        queue->front = queue->rear = -1; // Reset queue
    } else {
        queue->front++;
    }
    return node;
}

// Level order traversal using a queue
void levelOrderTraversal(Node* root) {
    if (root == NULL) return;

    Queue queue;
    initializeQueue(&queue);
    enqueue(&queue, root);

    while (!isEmpty(&queue)) {
        Node* current = dequeue(&queue);
        printf("%d ", current->data);

        if (current->llink != NULL) enqueue(&queue, current->llink);
        if (current->rlink != NULL) enqueue(&queue, current->rlink);
    }
}

// Example usage
int main() {
    Node* root = (Node*)malloc(sizeof(Node));
    root->data = 1;
    root->llink = (Node*)malloc(sizeof(Node));
    root->llink->data = 2;
    root->rlink = (Node*)malloc(sizeof(Node));
    root->rlink->data = 3;

    printf("Level-order traversal: ");
    levelOrderTraversal(root);
    printf("\n");

    return 0;
}
