#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define MAXSIZE 100

struct stack{
    int top  ;
    int items[MAXSIZE];
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

void push (struct stack *s, int c){
    if (isFull(s)){
        printf("Stack Overflow \n");
        return;
    }
    else {
        s->items[++(s->top)] = c;
    }
}

int pop (struct stack *s){
    if (isEmpty(s)){
        printf("Stack Underflow\n");
        return ('\0');
    }
    else {
        return (s->items[(s->top)--]);
    }
}

void toBase(int base, int num){
    struct stack s;
    init(&s);
    while (num!=0){
        int d = num%base;
        push(&s, d);
        num = num/base;
    }
    while (!isEmpty(&s)){
        int d = pop(&s);
        if (d < 10){
            printf("%d", d);
        }
        else {
            printf("%c", 'A' + d - 10);
        }
    }
}



int main(){
    int n;
    int base;
    printf("Enter a decimal number: ");
    scanf("%d", &n);
    printf("Enter base between 2 and 36: ");
    scanf ("%d", &base);
    if (base<2 || base>36){
        printf("Invalid Base ");
    }
    else {
        printf("Converted to Base %d: ", base);
        toBase(base,n);
    }

}
