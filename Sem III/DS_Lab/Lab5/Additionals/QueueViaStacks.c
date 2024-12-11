#include <stdio.h>
#include <stdlib.h>

#define MAX 100

typedef struct Stack {
    int top;
    int items[MAX];
} Stack;

void initializeStack(Stack *s) {
    s->top = -1;
}

int isEmpty(Stack *s) {
    return s->top == -1;
}

int isFull(Stack *s) {
    return s->top == MAX - 1;
}

void push(Stack *s, int item) {
    if (isFull(s)) {
        printf("Stack is full!\n");
        return;
    }
    s->items[++(s->top)] = item;
}

int pop(Stack *s) {
    if (isEmpty(s)) {
        printf("Stack is empty!\n");
        return -1;
    }
    return s->items[(s->top)--];
}

typedef struct Queue {
    Stack stack1;
    Stack stack2;
} Queue;

void initializeQueue(Queue *q) {
    initializeStack(&q->stack1);
    initializeStack(&q->stack2);
}

void enqueue(Queue *q, int item) {
    push(&q->stack1, item);
}

int dequeue(Queue *q) {
    int item;
    if (isEmpty(&q->stack2)) {
        while (!isEmpty(&q->stack1)) {
            push(&q->stack2, pop(&q->stack1));
        }
    }
    item = pop(&q->stack2);
    return item;
}

int main() {
    Queue q;
    initializeQueue(&q);

    enqueue(&q, 10);
    enqueue(&q, 20);
    enqueue(&q, 30);

    printf("Dequeued: %d\n", dequeue(&q));
    printf("Dequeued: %d\n", dequeue(&q));

    enqueue(&q, 40);
    printf("Dequeued: %d\n", dequeue(&q));
    printf("Dequeued: %d\n", dequeue(&q));

    return 0;
}
