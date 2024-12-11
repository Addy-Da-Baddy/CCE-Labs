#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int coeff;
    int exp;
    struct Node* next;
} Node;

typedef struct LinkedList {
    Node* head;
    int size;
} LinkedList;

Node* createNode(int coeff, int exp) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->coeff = coeff;
    newNode->exp = exp;
    newNode->next = NULL;
    return newNode;
}

void initList(LinkedList* list) {
    list->head = NULL;
    list->size = 0;
}

void appendTerm(LinkedList* poly, int coeff, int exp) {
    Node* newNode = createNode(coeff, exp);
    if (poly->head == NULL || poly->head->exp < exp) {
        newNode->next = poly->head;
        poly->head = newNode;
    } else {
        Node* temp = poly->head;
        while (temp->next != NULL && temp->next->exp >= exp) {
            temp = temp->next;
        }
        if (temp->exp == exp) {
            temp->coeff += coeff;
            free(newNode);
        } else {
            newNode->next = temp->next;
            temp->next = newNode;
        }
    }
    poly->size++;
}

void displayPoly(LinkedList* poly) {
    Node* temp = poly->head;
    while (temp != NULL) {
        if (temp->coeff != 0) {
            printf("%dx^%d", temp->coeff, temp->exp);
            if (temp->next != NULL && temp->next->coeff > 0) {
                printf(" + ");
            }
        }
        temp = temp->next;
    }
    printf("\n");
}

LinkedList* addPolynomials(LinkedList* poly1, LinkedList* poly2) {
    LinkedList* result = (LinkedList*)malloc(sizeof(LinkedList));
    initList(result);

    Node* p1 = poly1->head;
    Node* p2 = poly2->head;

    while (p1 != NULL) {
        appendTerm(result, p1->coeff, p1->exp);
        p1 = p1->next;
    }
    while (p2 != NULL) {
        appendTerm(result, p2->coeff, p2->exp);
        p2 = p2->next;
    }

    return result;
}

int main() {
    LinkedList poly1;
    LinkedList poly2;
    initList(&poly1);
    initList(&poly2);

    int choice, coeff, exp;

    do {
        printf("\nPolynomial Operations Menu:\n");
        printf("1. Add term to Polynomial 1\n");
        printf("2. Add term to Polynomial 2\n");
        printf("3. Display Polynomial 1\n");
        printf("4. Display Polynomial 2\n");
        printf("5. Add Polynomials\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter coefficient and exponent for Polynomial 1: ");
                scanf("%d %d", &coeff, &exp);
                appendTerm(&poly1, coeff, exp);
                break;
            case 2:
                printf("Enter coefficient and exponent for Polynomial 2: ");
                scanf("%d %d", &coeff, &exp);
                appendTerm(&poly2, coeff, exp);
                break;
            case 3:
                printf("Polynomial 1: ");
                displayPoly(&poly1);
                break;
            case 4:
                printf("Polynomial 2: ");
                displayPoly(&poly2);
                break;
            case 5: {
                LinkedList* result = addPolynomials(&poly1, &poly2);
                printf("Sum: ");
                displayPoly(result);
                free(result); // Free the memory for the result
                break;
            }
            case 6:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 6);

    return 0;
}

