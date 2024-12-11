#include <stdio.h>
#include <stdlib.h>

#define MAXSIZE 100

typedef struct Node {
    int data;
    struct Node* llink;
    struct Node* rlink;
} Node;

// Stack structure for storing nodes
typedef struct {
    Node* items[MAXSIZE];
    int top;
} Stack;

// Function to initialize the stack
void initializeStack(Stack* stack) {
    stack->top = -1;
}

// Function to check if the stack is empty
int isEmpty(Stack* stack) {
    return stack->top == -1;
}

// Function to push a node onto the stack
void push(Stack* stack, Node* node) {
    if (stack->top == MAXSIZE - 1) {
        printf("Stack overflow\n");
        return;
    }
    stack->items[++stack->top] = node;
}

// Function to pop a node from the stack
Node* pop(Stack* stack) {
    if (isEmpty(stack)) {
        return NULL;
    }
    return stack->items[stack->top--];
}

// Iterative inorder traversal
void inorderNonRecursive(Node* root) {
    Stack stack;
    initializeStack(&stack);
    Node* current = root;

    while (current != NULL || !isEmpty(&stack)) {
        while (current != NULL) {
            push(&stack, current);
            current = current->llink;
        }
        current = pop(&stack);
        printf("%d ", current->data);
        current = current->rlink;
    }
}

// Iterative preorder traversal
void preorderNonRecursive(Node* root) {
    if (root == NULL) return;

    Stack stack;
    initializeStack(&stack);
    push(&stack, root);

    while (!isEmpty(&stack)) {
        Node* current = pop(&stack);
        printf("%d ", current->data);

        if (current->rlink) push(&stack, current->rlink);
        if (current->llink) push(&stack, current->llink);
    }
}

// Iterative postorder traversal
void postorderNonRecursive(Node* root) {
    if (root == NULL) return;

    Stack stack1, stack2;
    initializeStack(&stack1);
    initializeStack(&stack2);

    push(&stack1, root);

    while (!isEmpty(&stack1)) {
        Node* current = pop(&stack1);
        push(&stack2, current);

        if (current->llink) push(&stack1, current->llink);
        if (current->rlink) push(&stack1, current->rlink);
    }

    while (!isEmpty(&stack2)) {
        Node* current = pop(&stack2);
        printf("%d ", current->data);
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
    
    root->llink->llink = (Node*)malloc(sizeof(Node));
    root->llink->llink->data = 4;
    
    root->llink->rlink = (Node*)malloc(sizeof(Node));
    root->llink->rlink->data = 5;
    
    root->rlink->llink = (Node*)malloc(sizeof(Node));
    root->rlink->llink->data = 6;
    
    root->rlink->rlink = (Node*)malloc(sizeof(Node));
    root->rlink->rlink->data = 7;
    
    root->llink->llink->llink = (Node*)malloc(sizeof(Node));
    root->llink->llink->llink->data = 8;
    
    root->llink->llink->rlink = (Node*)malloc(sizeof(Node));
    root->llink->llink->rlink->data = 9;
    
    root->llink->rlink->llink = (Node*)malloc(sizeof(Node));
    root->llink->rlink->llink->data = 10;

    printf("Non-recursive Inorder traversal: ");
    inorderNonRecursive(root);
    printf("\n");

    printf("Non-recursive Preorder traversal: ");
    preorderNonRecursive(root);
    printf("\n");

    printf("Non-recursive Postorder traversal: ");
    postorderNonRecursive(root);
    printf("\n");

    return 0;
}
