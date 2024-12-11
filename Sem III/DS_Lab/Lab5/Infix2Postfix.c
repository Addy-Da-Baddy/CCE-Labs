#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#define MAX 100

typedef struct stack {
    int top;
    char items[MAX];
} Stack;

void init(Stack *s) {
    s->top = -1;
}

bool isFull(Stack *s) {
    return (s->top == MAX - 1);
}

bool isEmpty(Stack *s) {
    return (s->top == -1);
}

void push(Stack *s, char c) {
    if (isFull(s)) {
        printf("Stack Overflow \n");
        return;
    } else {
        s->items[++(s->top)] = c;
    }
}

char pop(Stack *s) {
    if (isEmpty(s)) {
        printf("Stack Underflow\n");
        return '\0';
    } else {
        return s->items[(s->top)--];
    }
}

char peek(Stack *s) {
    if (!isEmpty(s)) {
        return s->items[s->top];
    } else {
        return '\0';
    }
}

bool isOperand(char c) {
    return ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9'));
}

int precedence(char op) {
    switch (op) {
        case '+':
        case '-':
            return 1;
        case '*':
        case '/':
            return 2;
        case '^':
            return 3;
        default:
            return 0;
    }
}

int main() {
    char infix[MAX];
    char postfix[MAX];

    printf("Enter an infix expression: ");

    gets(infix);

    Stack stack;
    init(&stack);

    int j = 0;

    for (int i = 0; infix[i] != '\0'; i++) {
        char token = infix[i];

        if (isOperand(token)) {
            postfix[j++] = token;
        } else if (token == '(') {
            push(&stack, token);
        } else if (token == ')') {
            while (!isEmpty(&stack) && peek(&stack) != '(') {
                postfix[j++] = pop(&stack);
            }
            pop(&stack);
        } else {
            while (!isEmpty(&stack) && precedence(peek(&stack)) >= precedence(token)) {
                postfix[j++] = pop(&stack);
            }
            push(&stack, token);
        }
    }

    while (!isEmpty(&stack)) {
        postfix[j++] = pop(&stack);
    }

    postfix[j] = '\0';

    printf("Postfix expression: ");
    puts(postfix);

    return 0;
}

