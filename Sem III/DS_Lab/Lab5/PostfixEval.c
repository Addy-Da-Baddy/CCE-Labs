#include <stdio.h>
#include <stdbool.h>
#include <math.h>

#define MAX 25

typedef struct stack {
    int top;
    int arr[MAX];
}st;

void init(st* s){
    s->top = -1;
}

bool isFull(st* s){
    return (s->top == MAX - 1);
}

bool isEmpty(st *s){
    return (s->top == -1);
}

void push(st *s, int n){
    if (!isFull(s)){
        s->top++;
        s->arr[s->top] = n;
    }
    else {
        printf("Full!\n");
    }
}

int pop(st *s){
    if (!isEmpty(s)){
        int x = s->arr[s->top];
        s->top--;
        return x;
    }
    printf("Stack Underflow\n");
    return -9999999;
}

int main(){
    st eval;
    char postfix[MAX];
    init(&eval);
    printf("Enter a Postfix Expression: ");
    gets(postfix);
    for (int i = 0; postfix[i]!='\0';i++){
        char token = postfix[i];
        if (token>='0'&&token<='9'){
            push(&eval,token - '0');
        }
        else {
            int val1 = pop(&eval);
            int val2 = pop(&eval);
            switch(token){
                case '+': push(&eval, val2 + val1); break;
                case '-': push(&eval, val2 - val1); break;
                case '*': push(&eval, val2 * val1); break;
                case '/': push(&eval, val2 / val1); break;
                case '^': push(&eval, (int)pow(val2,val1)); break;
                default: printf("Invalid Constant Detected"); return - 1;
            }
        }

    }

            printf("Answer of the expression: %d" , pop(&eval));
        return 0;
}
