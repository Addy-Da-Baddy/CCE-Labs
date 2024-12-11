#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct LinkedList {
    int size;
    Node* head;
} LL;

Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

void initList(LL* list) {
    list->head = NULL;
    list->size = 0;
}

void insertAfter(LL* list, int data, int prevData) {
    if (list->head == NULL) {
        printf("List is empty. Nowhere to insert after %d.\n", prevData);
        return;
    }

    Node* newNode = createNode(data);
    Node* temp = list->head;
    while (temp != NULL && temp->data != prevData) {
        temp = temp->next;
    }

    if (temp == NULL) {
        printf("No node with data %d found.\n", prevData);
        free(newNode);
    } else {
        newNode->next = temp->next;
        temp->next = newNode;
        list->size++;
    }
}

void insertBefore(LL* list, int data, int beforeData) {
    if (list->head == NULL) {
        printf("List is empty. Nowhere to insert before %d.\n", beforeData);
        return;
    }

    Node* newNode = createNode(data);
    if (list->head->data == beforeData) {
        newNode->next = list->head;
        list->head = newNode;
        list->size++;
        return;
    }

    Node* temp = list->head;
    while (temp->next != NULL && temp->next->data != beforeData) {
        temp = temp->next;
    }

    if (temp->next == NULL) {
        printf("No node with data %d found.\n", beforeData);
        free(newNode);
    } else {
        newNode->next = temp->next;
        temp->next = newNode;
        list->size++;
    }
}

void deleteData(LL* list, int data) {
    if (list->head == NULL) {
        printf("List is empty. Nothing to delete.\n");
        return;
    }

    if (list->head->data == data) {
        Node* oldHead = list->head;
        list->head = list->head->next;
        free(oldHead);
        list->size--;
        return;
    }

    Node* temp = list->head;
    Node* prev = NULL;
    while (temp != NULL && temp->data != data) {
        prev = temp;
        temp = temp->next;
    }

    if (temp == NULL) {
        printf("Node with data %d not found.\n", data);
    } else {
        prev->next = temp->next;
        free(temp);
        list->size--;
    }
}

void traverseList(LL* list) {
    Node* temp = list->head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

void reverseList(LL* list) {
    Node* prev = NULL;
    Node* current = list->head;
    Node* next = NULL;

    while (current != NULL) {
        next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    }

    list->head = prev;
}

void sortList(LL* list) {
    if (list->head == NULL) {
        return;
    }

    Node* i = NULL;
    Node* j = NULL;
    for (i = list->head; i != NULL; i = i->next) {
        for (j = i->next; j != NULL; j = j->next) {
            if (i->data > j->data) {
                int temp = i->data;
                i->data = j->data;
                j->data = temp;
            }
        }
    }
}

void deleteAlternateNodes(LL* list) {
    if (list->head == NULL) {
        return;
    }

    Node* current = list->head;
    Node* temp;

    while (current != NULL && current->next != NULL) {
        temp = current->next;
        current->next = temp->next;
        free(temp);
        current = current->next;
    }
}

void insertInSorted(LL* list, int data) {
    Node* newNode = createNode(data);
    if (list->head == NULL || list->head->data >= data) {
        newNode->next = list->head;
        list->head = newNode;
        list->size++;
        return;
    }

    Node* current = list->head;
    Node* prev = NULL;
    while (current != NULL && current->data < data) {
        prev = current;
        current = current->next;
    }

    newNode->next = current;
    prev->next = newNode;
    list->size++;
}

void displayMenu() {
    printf("\nMenu:\n");
    printf("1. Insert After\n");
    printf("2. Insert Before\n");
    printf("3. Delete Data\n");
    printf("4. Traverse List\n");
    printf("5. Reverse List\n");
    printf("6. Sort List\n");
    printf("7. Delete Alternate Nodes\n");
    printf("8. Insert in Sorted Order\n");
    printf("9. Exit\n");
}

int main() {
    LL list;
    initList(&list);
    int choice, data, prevData, beforeData;

    while (1) {
        displayMenu();
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter data to insert: ");
                scanf("%d", &data);
                printf("Enter the data of the node to insert after: ");
                scanf("%d", &prevData);
                insertAfter(&list, data, prevData);
                break;

            case 2:
                printf("Enter data to insert: ");
                scanf("%d", &data);
                printf("Enter the data of the node to insert before: ");
                scanf("%d", &beforeData);
                insertBefore(&list, data, beforeData);
                break;

            case 3:
                printf("Enter data to delete: ");
                scanf("%d", &data);
                deleteData(&list, data);
                break;

            case 4:
                printf("List contents: ");
                traverseList(&list);
                break;

            case 5:
                reverseList(&list);
                printf("List reversed.\n");
                break;

            case 6:
                sortList(&list);
                printf("List sorted.\n");
                break;

            case 7:
                deleteAlternateNodes(&list);
                printf("Deleted alternate nodes.\n");
                break;

            case 8:
                printf("Enter data to insert: ");
                scanf("%d", &data);
                insertInSorted(&list, data);
                break;

            case 9:
                printf("Exiting...\n");
                return 0;

            default:
                printf("Invalid choice. Please try again.\n");
                break;
        }
    }

    return 0;
}

