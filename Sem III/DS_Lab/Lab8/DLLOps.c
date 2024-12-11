#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct DoubleLLNode {
    int data;
    struct DoubleLLNode* rlink;
    struct DoubleLLNode* llink;
} Node;

typedef struct DoublyLinkedList {
    Node* head;
} DLL;

void initList(DLL* list);
Node* createNode(int data);
void insertRear(int data, DLL* list);
void deleteRear(DLL* list);
void printList(DLL* list);
void insertAtIndex(int data, DLL* list, int indx);
void deleteAtIndex(DLL* list, int indx);
void insertAfterElement(int data, int element, DLL* list);
void insertBeforeElement(int data, int element, DLL* list);
void traverseList(DLL* list);
void reverseList(DLL* list);

int main() {
    DLL list;
    initList(&list);
    int choice, data, index, element;

    do {
        printf("\nDoubly Linked List Menu:\n");
        printf("1. Insert at Rear\n");
        printf("2. Delete at Rear\n");
        printf("3. Print List\n");
        printf("4. Insert at Index\n");
        printf("5. Delete at Index\n");
        printf("6. Insert After Element\n");
        printf("7. Insert Before Element\n");
        printf("8. Traverse List\n");
        printf("9. Reverse List\n");
        printf("10. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter data to insert at rear: ");
                scanf("%d", &data);
                insertRear(data, &list);
                break;
            case 2:
                deleteRear(&list);
                break;
            case 3:
                printList(&list);
                break;
            case 4:
                printf("Enter data and index: ");
                scanf("%d %d", &data, &index);
                insertAtIndex(data, &list, index);
                break;
            case 5:
                printf("Enter index to delete: ");
                scanf("%d", &index);
                deleteAtIndex(&list, index);
                break;
            case 6:
                printf("Enter data and element to insert after: ");
                scanf("%d %d", &data, &element);
                insertAfterElement(data, element, &list);
                break;
            case 7:
                printf("Enter data and element to insert before: ");
                scanf("%d %d", &data, &element);
                insertBeforeElement(data, element, &list);
                break;
            case 8:
                traverseList(&list);
                break;
            case 9:
                reverseList(&list);
                break;
            case 10:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 10);

    return 0;
}


void initList(DLL* list) {
    list->head = NULL;
}

Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->data = data;
    newNode->llink = newNode->rlink = NULL;
    return newNode;
}

void insertRear(int data, DLL* list) {
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

void deleteRear(DLL* list) {
    if (list->head == NULL) {
        printf("List Empty!\n");
        return;
    }
    if (list->head->rlink == NULL) {
        Node* temp = list->head;
        list->head = NULL;
        free(temp);
        return;
    } else {
        Node* temp = list->head;
        while (temp->rlink != NULL) {
            temp = temp->rlink;
        }
        Node* prev = temp->llink;
        prev->rlink = NULL;
        free(temp);
    }
}

void printList(DLL* list) {
    Node* temp = list->head;
    if (list->head == NULL) {
        printf("List is empty.\n");
        return;
    }
    printf("NULL<--->");
    while (temp != NULL) {
        printf("%d<--->", temp->data);
        temp = temp->rlink;
    }
    printf("NULL\n");
}

void insertAtIndex(int data, DLL* list, int indx) {
    Node* newNode = createNode(data);

    if (indx == 0) {
        newNode->rlink = list->head;
        if (list->head != NULL) {
            list->head->llink = newNode;
        }
        list->head = newNode;
        return;
    }

    Node* temp = list->head;
    for (int i = 0; i < indx - 1; i++) {
        if (temp == NULL) {
            printf("Index out of bounds\n");
            free(newNode);
            return;
        }
        temp = temp->rlink;
    }

    if (temp == NULL) {
        printf("Index out of bounds\n");
        free(newNode);
        return;
    }

    Node* next = temp->rlink;
    temp->rlink = newNode;
    newNode->llink = temp;
    newNode->rlink = next;
    if (next != NULL) {
        next->llink = newNode;
    }
}

void deleteAtIndex(DLL* list, int indx) {
    if (list->head == NULL) {
        printf("List Empty\n");
        return;
    }
    if (indx == 0) {
        Node* prevHead = list->head;
        list->head = prevHead->rlink;
        if (list->head != NULL) {
            list->head->llink = NULL;
        }
        free(prevHead);
        return;
    }

    Node* temp = list->head;
    for (int i = 0; i < indx - 1; i++) {
        if (temp == NULL) {
            printf("Index out of bounds\n");
            return;
        }
        temp = temp->rlink;
    }

    if (temp == NULL || temp->rlink == NULL) {
        printf("Index out of bounds\n");
        return;
    }
    Node* toDelete = temp->rlink;
    temp->rlink = toDelete->rlink;
    if (toDelete->rlink != NULL) {
        toDelete->rlink->llink = temp;
    }
    free(toDelete);
}

void insertAfterElement(int data, int element, DLL* list) {
    Node* temp = list->head;
    while (temp != NULL && temp->data != element) {
        temp = temp->rlink;
    }
    if (temp == NULL) {
        printf("No such element exists\n");
        return;
    }

    Node* newNode = createNode(data);
    Node* next = temp->rlink;
    newNode->llink = temp;
    temp->rlink = newNode;
    if (next != NULL) {
        newNode->rlink = next;
        next->llink = newNode;
    }
}

void insertBeforeElement(int data, int element, DLL* list) {
    Node* temp = list->head;
    while (temp != NULL && temp->data != element) {
        temp = temp->rlink;
    }
    if (temp == NULL) {
        printf("No such element exists\n");
        return;
    }

    Node* newNode = createNode(data);
    if (list->head->data == element) {
        newNode->rlink = list->head;
        list->head->llink = newNode;
        list->head = newNode;
        return;
    }

    newNode->rlink = temp;
    newNode->llink = temp->llink;
    temp->llink = newNode;
    if (newNode->llink != NULL) {
        newNode->llink->rlink = newNode;
    }
}

void traverseList(DLL* list) {
    Node* temp = list->head;
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->rlink;
    }
    printf("\n");
}

void reverseList(DLL* list) {
    if (list->head == NULL) {
        printf("List is empty.\n");
        return;
    }

    Node* current = list->head;
    Node* temp = NULL;

    while (current != NULL) {

        temp = current->llink;
        current->llink = current->rlink;
        current->rlink = temp;

        current = current->llink;
    }

    if (temp != NULL) {
        list->head = temp->llink;
    }
}

