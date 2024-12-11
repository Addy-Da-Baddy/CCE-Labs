#include <stdio.h>
#include <stdlib.h> // Include for malloc and free functions

// Define the Node structure
typedef struct Node {
    int data;
    struct Node* next; // Correct the pointer type
} Node;

// Define the LinkedList structure
typedef struct LinkedList {
    int size;
    Node* head;
} LL;

// Function to create a new node
Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node)); // Corrected malloc and sizeof syntax
    if (newNode == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

// Function to initialize the linked list
void initList(LL* list) {
    list->head = NULL;
    list->size = 0;
}

// Function to append a new node to the list
void append(LL* list, int data) {
    Node* newNode = createNode(data);
    if (list->head == NULL) { // Use list instead of LL
        list->head = newNode;
    } else {
        Node* temp = list->head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = newNode;
    }
    list->size++; // Correct increment syntax
}

// Function to insert a node at a specific index
void insert(LL* list, int index, int data) {
    if (index < 0 || index > list->size) {
        printf("Out of bounds!\n");
        return;
    }
    Node* newNode = createNode(data);
    if (index == 0) {
        newNode->next = list->head;
        list->head = newNode;
    } else {
        Node* temp = list->head;
        for (int i = 1; i < index; i++) { // Correct variable name from 'position' to 'index'
            temp = temp->next;
        }
        newNode->next = temp->next;
        temp->next = newNode;
    }
    list->size++;
}

// Function to find the index of a node by value
int indexOf(LL* list, int key) {
    Node* temp = list->head;
    for (int i = 0; i < list->size; i++) {
        if (temp->data == key) { // Correct 'temp->key' to 'temp->data == key'
            return i;
        }
        temp = temp->next;
    }
    return -1;
}

// Function to delete a node at a specific index
void deleteIndex(LL* list, int index) {
    if (index < 0 || index >= list->size) { // Correct index range check
        printf("Out of bounds!\n");
        return;
    }
    Node* temp = list->head;
    if (index == 0) {
        list->head = temp->next;
        free(temp);
    } else {
        Node* prev = NULL;
        for (int i = 0; i < index; i++) { // Correct variable name from 'position' to 'index'
            prev = temp;
            temp = temp->next;
        }
        prev->next = temp->next;
        free(temp);
    }
    list->size--;
}

// Function to delete a node by its value
void deleteValue(LL* list, int key) {
    int index = indexOf(list, key);
    if (index == -1) {
        printf("Does not exist!\n");
    } else {
        deleteIndex(list, index);
    }
}

// Function to print the linked list
void printList(const LL* list) {
    Node* temp = list->head;
    while (temp != NULL) {
        printf("%d", temp->data);
        temp = temp->next;
        if (temp != NULL) { // Only print '->' if there is a next node
            printf(" -> ");
        }
    }
    printf("\n"); // Move to a new line after printing the list
}


void sortList(LL* list) {
    if (list->head == NULL || list->head->next == NULL) 
        return;

    Node* current;
    Node* index;
    int temp;

    for (current = list->head; current != NULL; current = current->next) {
        for (index = current->next; index != NULL; index = index->next) {
            if (current->data > index->data) {
                temp = current->data;
                current->data = index->data;
                index->data = temp;
            }
        }
    }
}


// Main function to test the implementation
int main() {
    LL list;
    initList(&list);

    append(&list, 10);
    append(&list, 20);
    append(&list, 30);
    printList(&list);

    insert(&list, 0, 15);
    printList(&list);

    deleteIndex(&list, 2);
    printList(&list);

    deleteValue(&list, 10);
    printList(&list);

    return 0;
}
