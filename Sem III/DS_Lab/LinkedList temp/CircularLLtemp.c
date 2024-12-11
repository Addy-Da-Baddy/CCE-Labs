#include <stdio.h>
#include <stdlib.h> // Include for malloc and free functions

// Define the Node structure
typedef struct Node {
    struct Node* next;
    int data;
} Node;

// Define the CircularLinkedList structure
typedef struct CircularLL {
    Node* head;
    Node* rear;
} CLL;

// Function to initialize the circular linked list
void initList(CLL* list) {
    list->head = NULL;
    list->rear = NULL;
}

// Function to create a new node
Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    newNode->data = data;
    return newNode;
}

// Function to append a new node at the front of the list
void appendFront(CLL* list, int data) {
    Node* newNode = createNode(data);
    if (list->head == NULL) {
        // List is empty
        list->head = newNode;
        list->rear = newNode;
        newNode->next = newNode; // Point to itself
    } else {
        newNode->next = list->head;
        list->head = newNode;
        list->rear->next = list->head; // Update the rear to point to new head
    }
}

// Function to append a new node at the end of the list without using list->head
void appendEnd(CLL* list, int data) {
    Node* newNode = createNode(data); // Create the new node
    if (list->rear == NULL) {
        // List is empty
        list->head = newNode;
        list->rear = newNode;
        newNode->next = newNode; // Point to itself
    } else {
        newNode->next = list->head; // New node points to head (circular)
        list->rear->next = newNode; // Rear points to the new node
        list->rear = newNode; // Update the rear to the new node
    }
}

// Function to print the circular linked list
void printList(const CLL* list) {
    if (list->head == NULL) {
        printf("List is empty\n");
        return;
    }

    Node* temp = list->head;
    do {
        printf("%d", temp->data);
        temp = temp->next;
        if (temp != list->head) {
            printf(" -> ");
        }
    } while (temp != list->head);
    printf("\n");
}

// Main function to test the implementation
int main() {
    CLL list;
    initList(&list);

    appendEnd(&list, 10);
    appendEnd(&list, 20);
    appendEnd(&list, 30);
    printList(&list);

    appendFront(&list, 5);
    appendFront(&list, 1);
    printList(&list);

    return 0;
}
