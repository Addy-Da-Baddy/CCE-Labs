#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct LinkedList {
    struct Node* head;
} LL;

void initList(LL* list) {
    list->head = NULL;
}

Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

void appendNode(LL* list, int data) {
    Node* newNode = createNode(data);
    if (list->head == NULL) {
        list->head = newNode;
    } else {
        Node* temp = list->head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = newNode;
    }
}

void mergeLists(LL* list1, LL* list2, LL* list3) {
    initList(list3);
    Node* temp1 = list1->head;
    Node* temp2 = list2->head;
    
    while (temp1 != NULL && temp2 != NULL) {
        appendNode(list3, temp1->data);
        temp1 = temp1->next;
        appendNode(list3, temp2->data);
        temp2 = temp2->next;
    }
    
    while (temp1 != NULL) {
        appendNode(list3, temp1->data);
        temp1 = temp1->next;
    }
    
    while (temp2 != NULL) {
        appendNode(list3, temp2->data);
        temp2 = temp2->next;
    }
}

void printList(LL* list) {
    Node* temp = list->head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

int main() {
    LL list1, list2, list3;
    initList(&list1);
    initList(&list2);

    int n, val;

    printf("Enter number of elements in first list: ");
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        printf("Enter value %d: ", i + 1);
        scanf("%d", &val);
        appendNode(&list1, val);
    }

    printf("Enter number of elements in second list: ");
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        printf("Enter value %d: ", i + 1);
        scanf("%d", &val);
        appendNode(&list2, val);
    }

    mergeLists(&list1, &list2, &list3);

    printf("Merged List: ");
    printList(&list3);

    return 0;
}
