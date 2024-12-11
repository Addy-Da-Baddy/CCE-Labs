#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* rlink;
    struct Node* llink;
} Node;

typedef struct DLL {
    Node* head;
} DLL;

void initList(DLL* list) {
    list->head = NULL;
}

Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    newNode->data = data;
    newNode->rlink = NULL;
    newNode->llink = NULL;
    return newNode;
}

void AppendEnd(int data, DLL* list) {
    Node* newNode = createNode(data);
    if (list->head == NULL) {
        list->head = newNode;
    } else {
        Node* temp = list->head;
        while (temp->rlink != NULL) {
            temp = temp->rlink;
        }
        temp->rlink = newNode;
        newNode->llink = temp;
    }
}

void AppendStart(int data, DLL* list) {
    Node* newNode = createNode(data);
    if (list->head == NULL) {
        list->head = newNode;
    } else {
        Node* oldHead = list->head;
        newNode->rlink = oldHead;
        oldHead->llink = newNode;
        list->head = newNode;
    }
}

void DeleteStart(DLL* list) {
    if (list->head == NULL) {
        printf("Empty List!\n");
        return;
    }
    if (list->head->rlink == NULL) {
        Node* oldHead = list->head;
        list->head = NULL;
        free(oldHead);
        return;
    }
    Node* oldHead = list->head;
    Node* newHead = oldHead->rlink;
    list->head = newHead;
    newHead->llink = NULL;
    free(oldHead);
}

void DeleteEnd(DLL* list) {
    if (list->head == NULL) {
        printf("Empty List!\n");
        return;
    }
    if (list->head->rlink == NULL) {
        Node* oldHead = list->head;
        list->head = NULL;
        free(oldHead);
        return;
    }
    Node* temp = list->head;
    while (temp->rlink != NULL) {
        temp = temp->rlink;
    }
    Node* prev = temp->llink;
    prev->rlink = NULL;
    free(temp);
}

// Print list from start to end
void printListForward(DLL* list) {
    if (list->head == NULL) {
        printf("List is empty!\n");
        return;
    }
    Node* temp = list->head;
    printf("List (forward): ");
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->rlink;
    }
    printf("\n");
}

// Print list from end to start
void printListBackward(DLL* list) {
    if (list->head == NULL) {
        printf("List is empty!\n");
        return;
    }
    Node* temp = list->head;
    // Traverse to the last node
    while (temp->rlink != NULL) {
        temp = temp->rlink;
    }
    printf("List (backward): ");
    // Traverse backward using the llink
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->llink;
    }
    printf("\n");
}

int main() {
    DLL list;
    initList(&list);

    AppendEnd(10, &list);
    AppendEnd(20, &list);
    AppendStart(5, &list);

    printListForward(&list);   // Expected output: 5 10 20
    printListBackward(&list);  // Expected output: 20 10 5

    DeleteStart(&list);
    printListForward(&list);   // Expected output: 10 20
    printListBackward(&list);  // Expected output: 20 10

    DeleteEnd(&list);
    printListForward(&list);   // Expected output: 10
    printListBackward(&list);  // Expected output: 10

    return 0;
}
