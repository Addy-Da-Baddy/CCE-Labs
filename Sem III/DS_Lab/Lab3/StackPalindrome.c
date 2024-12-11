#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define MAXSIZE 100

struct stack{
    int top  ;
    char items[MAXSIZE];
};

void init(struct stack *s){
    s->top = -1;
}

bool isFull(struct stack *s){
    return (s->top==MAXSIZE-1);
}

bool isEmpty(struct stack *s){
    return (s->top == -1);
}

void push (struct stack *s, char c){
    if (isFull(s)){
        printf("Stack Overflow \n");
        return;
    }
    else {
        s->items[++s->top] = c;
    }
}

char pop (struct stack *s){
    if (isEmpty(s)){
        printf("Stack Underflow\n");
        return ('\0');
    }
    else {
        return (s->items[s->top--]);
    }
}




int main(){
    char str[MAXSIZE];
    printf("Enter a string: ");
    gets(str);
    struct stack s;
    init(&s);
    for (int i = 0; str[i]!='\0'; i++)
        push(&s,str[i]);
    for (int i = 0; str[i]!='\0'; i++){
        char c = pop(&s);
        if (c!=str[i]){
            printf("Not a palindrome");
            return 0;
        }
    }

    printf("Palindrome");
    return 0;
}
