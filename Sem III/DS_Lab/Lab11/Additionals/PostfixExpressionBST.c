#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

typedef struct tnode {
    struct tnode* llink;
    struct tnode* rlink;
    char data;
} tnode;

tnode* createNode(char value) {
    tnode* newNode = (tnode*)malloc(sizeof(tnode));
    newNode->data = value;
    newNode->llink = NULL;
    newNode->rlink = NULL;
    return newNode;
}

tnode* constructTree(char* postfix) {
    tnode* stack[100];
    int top = -1;

    for (int i = 0; postfix[i]; i++) {
        if (isalnum(postfix[i])) {
            stack[++top] = createNode(postfix[i]);
        } else {
            tnode* node = createNode(postfix[i]);
            node->rlink = stack[top--];
            node->llink = stack[top--];
            stack[++top] = node;
        }
    }
    return stack[top];
}

int evaluate(tnode* root) {
    if (!root) return 0;
    if (isdigit(root->data)) return root->data - '0';

    int leftEval = evaluate(root->llink);
    int rightEval = evaluate(root->rlink);

    switch (root->data) {
        case '+': return leftEval + rightEval;
        case '-': return leftEval - rightEval;
        case '*': return leftEval * rightEval;
        case '/': return leftEval / rightEval;
    }
    return 0;
}

int main() {
    char postfix[100]; // Buffer for user input

    printf("Enter a postfix expression: ");
    fgets(postfix, sizeof(postfix), stdin); // Read user input

    // Remove newline character if present
    size_t len = strlen(postfix);
    if (len > 0 && postfix[len - 1] == '\n') {
        postfix[len - 1] = '\0';
    }

    tnode* root = constructTree(postfix);
    printf("Result of expression: %d\n", evaluate(root));

    return 0;
}
