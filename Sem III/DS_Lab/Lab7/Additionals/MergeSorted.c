#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct List {
    int currentSize;
    Node* head;
} List;

Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

void initList(List* list) {
    list->currentSize = 0;
    list->head = NULL;
}

void appendList(List* listA, List* listB) {
    if (listA->head == NULL) {
        listA->head = listB->head;
    } else {
        Node* temp = listA->head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = listB->head;
    }
    listA->currentSize += listB->currentSize;
    listB->head = NULL;
    listB->currentSize = 0;
}

void bubbleSort(List* list) {
    if (list->head == NULL) return;

    int swapped;
    Node *ptr1;
    Node *lptr = NULL;

    do {
        swapped = 0;
        ptr1 = list->head;

        while (ptr1->next != lptr) {
            if (ptr1->data > ptr1->next->data) {
                int temp = ptr1->data;
                ptr1->data = ptr1->next->data;
                ptr1->next->data = temp;
                swapped = 1;
            }
            ptr1 = ptr1->next;
        }
        lptr = ptr1;
    } while (swapped);
}

void printList(List* list) {
    Node* temp = list->head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

int main() {
    List listX, listY;
    initList(&listX);
    initList(&listY);

    int n, val;

    printf("Enter the number of elements in the first list: ");
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        printf("Enter value %d for list 1: ", i + 1);
        scanf("%d", &val);
        if (listX.head == NULL) {
            listX.head = createNode(val);
        } else {
            Node* temp = listX.head;
            while (temp->next != NULL) {
                temp = temp->next;
            }
            temp->next = createNode(val);
        }
        listX.currentSize++;
    }

    printf("Enter the number of elements in the second list: ");
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        printf("Enter value %d for list 2: ", i + 1);
        scanf("%d", &val);
        if (listY.head == NULL) {
            listY.head = createNode(val);
        } else {
            Node* temp = listY.head;
            while (temp->next != NULL) {
                temp = temp->next;
            }
            temp->next = createNode(val);
        }
        listY.currentSize++;
    }

    appendList(&listX, &listY);
    bubbleSort(&listX);

    printf("Sorted Merged List: ");
    printList(&listX);

    return 0;
}

