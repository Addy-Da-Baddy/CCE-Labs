#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct tnode {
    struct tnode* llink;
    struct tnode* rlink;
    int data;
} tnode;

typedef struct Queue {
    tnode* nodes[100];
    int front;
    int rear;
} Queue;

void enqueue(Queue* q, tnode* node) {
    if (q->rear < 100) { // Check if the queue is not full
        q->nodes[q->rear++] = node;
    }
}

tnode* dequeue(Queue* q) {
    if (!isEmpty(q)) {
        return q->nodes[q->front++];
    }
    return NULL; // Return NULL if the queue is empty
}

bool isEmpty(Queue* q) {
    return q->front == q->rear;
}

tnode* createNode(int value) {
    tnode* newNode = (tnode*)malloc(sizeof(tnode));
    newNode->data = value;
    newNode->llink = NULL;
    newNode->rlink = NULL;
    return newNode;
}

tnode* insert(tnode* root, int value) {
    if (root == NULL) {
        return createNode(value);
    }
    if (value < root->data) {
        root->llink = insert(root->llink, value);
    } else {
        root->rlink = insert(root->rlink, value);
    }
    return root;
}

void levelOrder(tnode* root) {
    if (root == NULL) return;

    Queue q = { .front = 0, .rear = 0 };
    enqueue(&q, root);

    while (!isEmpty(&q)) {
        tnode* current = dequeue(&q);
        printf("%d ", current->data);

        if (current->llink) enqueue(&q, current->llink);
        if (current->rlink) enqueue(&q, current->rlink);
    }
}

int main() {
    tnode* root = NULL;
    root = insert(root, 50);
    insert(root, 30);
    insert(root, 20);
    insert(root, 40);
    insert(root, 70);
    insert(root, 60);
    insert(root, 80);

    printf("Level Order Traversal: ");
    levelOrder(root);
    printf("\n");

    return 0;
}
