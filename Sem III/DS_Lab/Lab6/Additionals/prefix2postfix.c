#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#define MAX 100

typedef struct stack {
    int top;
    char items[MAX][MAX];
} Stack;

// Stack operations for strings
void init(Stack *s) {
    s->top = -1;
}

bool isFull(Stack *s) {
    return (s->top == MAX - 1);
}

bool isEmpty(Stack *s) {
    return (s->top == -1);
}

void push(Stack *s, const char* c) {
    if (isFull(s)) {
        printf("Stack Overflow \n");
        return;
    } else {
        strcpy(s->items[++(s->top)], c);
    }
}

void pop(Stack *s, char *value) {
    if (isEmpty(s)) {
        printf("Stack Underflow\n");
        return;
    } else {
        strcpy(value, s->items[(s->top)--]);
    }
}

// Stack operations for characters
typedef struct char_stack {
    int top;
    char items[MAX];
} CharStack;

void initCharStack(CharStack *s) {
    s->top = -1;
}

bool isFullCharStack(CharStack *s) {
    return (s->top == MAX - 1);
}

bool isEmptyCharStack(CharStack *s) {
    return (s->top == -1);
}

void pushChar(CharStack *s, char c) {
    if (isFullCharStack(s)) {
        printf("Stack Overflow \n");
        return;
    } else {
        s->items[++(s->top)] = c;
    }
}

char popChar(CharStack *s) {
    if (isEmptyCharStack(s)) {
        printf("Stack Underflow\n");
        return '\0';
    } else {
        return s->items[(s->top)--];
    }
}

char peekChar(CharStack *s) {
    if (!isEmptyCharStack(s)) {
        return s->items[s->top];
    } else {
        return '\0';
    }
}

bool isOperator(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/' || c == '^';
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

void reverseString(char* str) {
    int n = strlen(str);
    for (int i = 0; i < n / 2; i++) {
        char temp = str[i];
        str[i] = str[n - i - 1];
        str[n - i - 1] = temp;
    }
}

void prefixToInfix(const char *prefix, char *infix) {
    Stack stack;
    init(&stack);
    char reversedPrefix[MAX];
    char temp[MAX];

    strcpy(reversedPrefix, prefix);
    reverseString(reversedPrefix);

    for (int i = 0; reversedPrefix[i] != '\0'; i++) {
        char token = reversedPrefix[i];
        if (!isOperator(token)) {
            char oprnd[2] = {token, '\0'};
            push(&stack, oprnd);
        } else {
            char val1[MAX];
            char val2[MAX];
            pop(&stack, val2);
            pop(&stack, val1);

            snprintf(temp, sizeof(temp), "(%s %c %s)", val1, token, val2);
            push(&stack, temp);
        }
    }

    pop(&stack, infix);
}

void infixToPostfix(const char *infix, char *postfix) {
    CharStack stack;
    initCharStack(&stack);
    int j = 0;

    for (int i = 0; infix[i] != '\0'; i++) {
        char token = infix[i];

        if (token == ' ') continue;

        if (isOperator(token)) {
            while (!isEmptyCharStack(&stack) && precedence(peekChar(&stack)) >= precedence(token)) {
                postfix[j++] = popChar(&stack);
                postfix[j++] = ' ';
            }
            pushChar(&stack, token);
        } else if (token == '(') {
            pushChar(&stack, token);
        } else if (token == ')') {
            while (!isEmptyCharStack(&stack) && peekChar(&stack) != '(') {
                postfix[j++] = popChar(&stack);
                postfix[j++] = ' ';
            }
            popChar(&stack); // Remove '('
        } else {
            postfix[j++] = token;
            postfix[j++] = ' ';
        }
    }

    while (!isEmptyCharStack(&stack)) {
        postfix[j++] = popChar(&stack);
        postfix[j++] = ' ';
    }

    postfix[j] = '\0';
}

int main() {
    char prefix[MAX];
    char infix[MAX];
    char postfix[MAX];

    printf("Enter a prefix expression: ");
    gets(prefix); // Safe usage in your environment

    prefixToInfix(prefix, infix);
    printf("Infix expression: %s\n", infix);

    infixToPostfix(infix, postfix);
    printf("Postfix expression: %s\n", postfix);

    return 0;
}
