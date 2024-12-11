#include <stdio.h>
#include <stdlib.h>

// Define the Node structure
typedef struct Node {
    int data;
    struct Node* next;
} Node;

// Define the Stack structure
typedef struct Stack {
    Node* top;
    int size;
} Stack;

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

// Function to initialize a stack
void initStack(Stack* stack) {
    stack->top = NULL;
    stack->size = 0;
}

// Function to push an element onto the stack
void push(Stack* stack, int data) {
    Node* newNode = createNode(data);
    newNode->next = stack->top;
    stack->top = newNode;
    stack->size++;
}

// Function to pop an element from the stack
int pop(Stack* stack) {
    if (stack->top == NULL) {
        printf("Stack underflow\n");
        exit(1);
    }
    Node* temp = stack->top;
    int data = temp->data;
    stack->top = stack->top->next;
    free(temp);
    stack->size--;
    return data;
}

// Function to peek at the top element of the stack
int peek(const Stack* stack) {
    if (stack->top == NULL) {
        printf("Stack is empty\n");
        exit(1);
    }
    return stack->top->data;
}

// Function to print the stack
void printStack(const Stack* stack) {
    Node* temp = stack->top;
    while (temp != NULL) {
        printf("%d", temp->data);
        temp = temp->next;
        if (temp != NULL) {
            printf(" -> ");
        }
    }
    printf("\n");
}

// Main function to test the stack implementation
int main() {
    Stack stack;
    initStack(&stack);

    // Push elements onto the stack
    push(&stack, 10);
    push(&stack, 20);
    push(&stack, 30);
    
    printf("Stack after pushes:\n");
    printStack(&stack);

    // Peek the top element
    printf("Top element: %d\n", peek(&stack));

    // Pop elements from the stack
    printf("Popped element: %d\n", pop(&stack));
    printf("Popped element: %d\n", pop(&stack));
    
    printf("Stack after pops:\n");
    printStack(&stack);

    return 0;
}
