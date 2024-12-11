#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define MAX 100

typedef struct stack{
    int top;
    char items[MAX];
} stack ;

void init (stack *s){
    s->top = -1;
}

bool isFull(stack *s){
    return (s->top == MAX-1);
}

bool isEmpty(stack *s){
    return (s->top==-1);
}

void push(stack *s, char c){
    if (!isFull(s)){
        s->top++;
        s->items[s->top] = c;
    }
}

char pop (stack *s){
    if (!isEmpty(s)){
        char val = s->items[s->top];
        s->top--;
        return(val);
    }
    else {
        return '\0';
    }
}

char peek(stack *s){
    if (!isEmpty(s)){
        return (s->items[s->top]);
    }
    else {
        return '\0';
    }
}

bool isOperand(char c){
  return ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9'));
}

int precedence(char op){
    switch(op){
        case '+':
        case '-' : return 1;
        case '*' :
        case '/': return 2;
        case '^': return 3;
        default: return 0;
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

int main(){
    char prefix[MAX];
    char infix[MAX];
    stack s;
    init(&s);
    printf("Enter an Infix Expression: ");
    gets(infix);
    int j = 0;
    int i = 0;


    for (i = 0; infix[i]!= '\0'; i++){
        if (infix[i]==')'){
            infix[i]='(';
        }
        else if(infix[i]=='('){
            infix[i] = ')';
        }
    }
    reverseString(infix);

    puts(infix);






    for (i = 0; infix[i] != '\0'; i++){
        char token = infix[i];
        if ((isOperand(token))){
            prefix[j++] = token;
        }
        else {
            if (token == '('){
                    push(&s,token);
                }
            else if (token == ')'){
                while(!isEmpty(&s) && peek(&s)!='('){
                        prefix[j++] = pop(&s);
                      }
                pop(&s);
            }
            else {
                while(!isEmpty(&s) && precedence(peek(&s))>precedence(token)){
                    prefix[j++] = pop(&s);
                }

                push(&s,token);
            }
        }
    }

     while (!isEmpty(&s)) {
        prefix[j++] = pop(&s);
    }



    reverseString(prefix);

    prefix[j] = '\0';

    printf("Prefix expression: ");
    puts(prefix);

    return 0;
}


