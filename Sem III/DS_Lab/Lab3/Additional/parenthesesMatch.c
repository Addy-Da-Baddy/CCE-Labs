#include <stdio.h>
#include <stdbool.h>

#define MAX_SIZE 100

struct stack {
    char arr[MAX_SIZE];
    int top;
};

void init(struct stack* s) {
    s->top = -1;
}

bool isFull(struct stack* s) {
    return s->top == MAX_SIZE - 1;
}

bool isEmpty(struct stack* s) {
    return s->top == -1;
}

void push(struct stack* s, char c) {
    if (isFull(s)) {
        printf("Stack overflow!\n");
    } else {
        s->arr[++s->top] = c;
    }
}

char pop(struct stack* s) {
    if (isEmpty(s)) {
        printf("Stack underflow!\n");
        return '\0';
    } else {
        return s->arr[s->top--];
    }
}

bool isOpening(char c) {
    return c == '(' || c == '{' || c == '[';
}

bool isClosing(char c) {
    return c == ')' || c == '}' || c == ']';
}

bool isMatchingPair(char opening, char closing) {
    return (opening == '(' && closing == ')') ||
           (opening == '{' && closing == '}') ||
           (opening == '[' && closing == ']');
}

bool isValidExpression(char* expression) {
    struct stack s;
    init(&s);

    for (int i = 0; expression[i] != '\0'; i++) {
        char c = expression[i];
        if (isOpening(c)) {
            push(&s, c);
        } else if (isClosing(c)) {
            if (isEmpty(&s) || !isMatchingPair(pop(&s), c)) {
                return false;
            }
        }
    }

    return isEmpty(&s);
}

int main() {
    char expression[MAX_SIZE];
    printf("Enter an expression: ");
    scanf("%s", expression);

    if (isValidExpression(expression)) {
        printf("The expression is valid\n");
    } else {
        printf("The expression is not valid\n");
    }

    return 0;
}
