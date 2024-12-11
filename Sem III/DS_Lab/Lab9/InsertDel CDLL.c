#include <stdio.h>
#include <stdlib.h>

typedef struct Node{
    struct Node* llink;
    int data;
    struct Node* rlink;


}Node;

typedef struct DCLL{
    struct Node* head;
    struct Node* rear;
}DCLL;

Node* createNode(int data){
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->rlink = NULL;
    newNode->llink = NULL;
    newNode->data = data;
    return newNode;
}

void initList(DCLL* list){
    list->head = NULL;
    list->rear = NULL;
}

void insert(DCLL* list, int data, int index){
        Node* newNode = createNode(data);

        if (list->head==NULL || list->rear==NULL){
            list->head = newNode;
            list->rear = newNode;
            newNode->llink = newNode;
            newNode->rlink = newNode;
            return;
        }

        if (index == 0){
            newNode->rlink = list->head;
            list->head->llink = newNode;
            newNode->llink = list->rear;
            list->rear->rlink = newNode;
            list->head = newNode;
            return;
        }

        Node* curr = list->head;
        int currind = 0;
      while (currind !=index-1) {
        curr = curr->rlink;
        if (curr == list->head){
            printf("Out of range \n");
            return;
        }
        currind++;
    }
if (curr->rlink == list->head) {
    newNode->llink = list->rear;
    newNode->rlink = list->head;
    list->rear->rlink = newNode;
    list->head->llink = newNode;
    list->rear = newNode;
    return;
}


        Node* next = curr->rlink;
        curr->rlink = newNode;
        next->llink = newNode;
        newNode->rlink = next;
        newNode->llink = curr;

}


void deleleteElement (DCLL* list, int data){
    if (list->head == NULL){
        printf("Empty List! \n ");
        return;
    }
    Node* curr = list->head;
    do {
        if (curr->data == data){
            if (curr == list->head){
                if (list->head==list->rear){
                    free(list->head);
                    list->head = NULL;
                    list->rear = NULL;
                    return;
                }
                else {
                    list->rear->rlink = list->head->rlink;
                    list->head->rlink->llink = list->rear;
                    Node* oldHead = list->head;
                    list->head = oldHead->rlink;
                    free(oldHead);
                    return;
                }
            }

            curr->llink->rlink = curr->rlink;
            curr->rlink->llink = curr->llink;
            if (curr==list->rear){
                list->rear = curr->llink;
            }
            free(curr);
            return;
        }
        curr = curr->rlink;
    }while (curr!=list->head);
    printf("No such element found!");
}




void printList(DCLL* list) {
    if (list->head == NULL) return;
    Node* curr = list->head;
    do {
        printf("%d ", curr->data);
        curr = curr->rlink;
    } while (curr != list->head);
    printf("\n");
}

int main() {
    DCLL list;
    initList(&list);
    int choice, data, index;

    while (1) {
        printf("\nMenu:\n");
        printf("1. Insert\n");
        printf("2. Delete by element\n");
        printf("3. Print list\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter data to insert: ");
                scanf("%d", &data);
                printf("Enter index to insert at: ");
                scanf("%d", &index);
                insert(&list, data, index);
                break;

            case 2:
                printf("Enter element to delete: ");
                scanf("%d", &data);
                deleleteElement(&list, data);
                break;

            case 3:
                printList(&list);
                break;

            case 4:
                printf("Exiting...\n");
                exit(0);
                break;

            default:
                printf("Invalid choice, please try again.\n");
        }
    }

    return 0;
}
