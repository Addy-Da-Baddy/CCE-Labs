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

void reverseString(char* str) {
    int n = strlen(str);
    for (int i = 0; i < n / 2; i++) {
        char temp = str[i];
        str[i] = str[n - i - 1];
        str[n - i - 1] = temp;
    }
}


int main(){

    Stack stack;
    init(&stack);
    char prefix[MAX];
    printf("Enter a prefix expression: ");
    gets(prefix);
    reverseString(prefix);
    char infix[MAX];
    char temp[MAX];

    for (int i = 0; prefix[i]!='\0'; i++){
        char token = prefix[i];
        if (!isOperator(token)){
            char oprnd[2] = {token,'\0'};
            push (&stack,oprnd);
        }

        else {
            char val1[MAX];
            char val2[MAX];
            pop(&stack, val2);
            pop(&stack, val1);

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
