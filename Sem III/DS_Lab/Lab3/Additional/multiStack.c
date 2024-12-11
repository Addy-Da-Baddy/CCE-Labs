#include <stdio.h>
#include <stdbool.h>

#define MAXSIZE 20

struct multiStack {
    int top[MAXSIZE];             // Top pointers for each stack
    int boundary[MAXSIZE + 1];    // Boundary markers for each stack
    int items[MAXSIZE];           // Shared array for all stacks
    int numStacks;                // Number of stacks
};

void init(struct multiStack* ms, int numStacks) {
    ms->numStacks = numStacks;    // Store the number of stacks
    int size = MAXSIZE / numStacks; // Calculate the size of each stack

    for (int i = 0; i < numStacks; i++) {
        ms->top[i] = ms->boundary[i] = i * size - 1;
    }
    ms->boundary[numStacks] = MAXSIZE;
}

bool isFull(struct multiStack* ms, int stack_index) {
    return (ms->top[stack_index] == ms->boundary[stack_index + 1]);
}

bool isEmpty(struct multiStack* ms, int stack_index) {
    return (ms->top[stack_index] == ms->boundary[stack_index]);
}

void push(struct multiStack* ms, int stack_index, int num) {
    if (isFull(ms, stack_index)) {
        printf("Stack %d Overflow\n", stack_index);
    } else {
        ms->items[++ms->top[stack_index]] = num;
    }
}

int pop(struct multiStack* ms, int stack_index) {
    if (isEmpty(ms, stack_index)) {
        printf("Stack %d Underflow\n", stack_index);
        return -999999;  // Special error code
    } else {
        return ms->items[ms->top[stack_index]--];
    }
}

void printStacks(struct multiStack* ms) {
    printf("\nCurrent state of all stacks:\n");
    for (int i = 0; i < ms->numStacks; i++) {
        printf("Stack %d: ", i);
        if (isEmpty(ms, i)) {
            printf("(empty)\n");
        } else {
            for (int j = ms->boundary[i] + 1; j <= ms->top[i]; j++) {
                printf("%d ", ms->items[j]);
            }
            printf("\n");
        }
    }
    printf("\n");
}

int main() {
    struct multiStack ms;

    // Take user input for number of stacks
    int numStacks;
    printf("Enter the number of stacks (up to %d): ", MAXSIZE);
    scanf("%d", &numStacks);

    if (numStacks <= 0 || numStacks > MAXSIZE) {
        printf("Invalid number of stacks. Must be between 1 and %d.\n", MAXSIZE);
        return 1;
    }

    init(&ms, numStacks);  // Initialize the multi-stack with user input

    // Example operations for testing
    push(&ms, 0, 10);
    push(&ms, 0, 20);
    push(&ms, 1, 30);
    push(&ms, 1, 40);
    push(&ms, 2, 50);
    push(&ms, 2, 60);
    push(&ms, 2, 70);

    // Print all stacks after initial pushes
    printStacks(&ms);

    // Pop some items and show the state
    printf("Popped from stack 0: %d\n", pop(&ms, 0));
    printf("Popped from stack 1: %d\n", pop(&ms, 1));
    printf("Popped from stack 2: %d\n", pop(&ms, 2));

    // Print all stacks after popping
    printStacks(&ms);

    // Push more elements into different stacks
    push(&ms, 0, 80);
    push(&ms, 1, 90);
    push(&ms, 3, 100);  // If numStacks >= 4

    // Print the final state of all stacks
    printStacks(&ms);

    return 0;
}
