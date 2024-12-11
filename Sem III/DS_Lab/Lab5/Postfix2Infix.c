#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define MAX 100

typedef struct stack {
    int top;
    char items[MAX][MAX];
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

void push(Stack *s, char* c) {
    if (isFull(s)) {
        printf("Stack Overflow \n");
        return;
    } else {
        strcpy(s->items[++(s->top)],c);
    }
}

void pop(Stack *s, char *value) {
    if (isEmpty(s)) {
        printf("Stack Underflow\n");
        return '\0';
    } else {
         strcpy(value, s->items[(s->top)--]);
    }
}

int isOperator(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/' || c == '^';
}

int main(){

    Stack stack;
    init(&stack);
    char postfix[MAX];
    printf("Enter a postfix expression: ");
    gets(postfix);
    char infix[MAX];
    char temp[MAX];

    for (int i = 0; postfix[i]!='\0'; i++){
        char token = postfix[i];
        if (!isOperator(token)){
            char oprnd[2] = {token,'\0'};
            push (&stack,oprnd);
        }

        else {
            char val1[MAX];
            char val2[MAX];
            pop(&stack, val1);
            pop(&stack, val2);

            strcpy(temp, "(");
            strcat(temp, val2);
            char ops[2] = {token, '\0'};
            strcat(temp,ops);
            strcat(temp,val1);
            strcat(temp,")");
            push(&stack,temp);
        }
    }

    pop(&stack,infix);
      puts(infix);

    return 0;


}

