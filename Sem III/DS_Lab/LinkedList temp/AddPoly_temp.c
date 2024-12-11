#include <stdio.h>
#include <stdlib.h>

// Define the structure for a polynomial term (node)
typedef struct Node {
    int coeff;          // Coefficient
    int exp;            // Exponent
    struct Node* next;  // Pointer to the next term
} Node;

// Define the structure for the linked list (polynomial)
typedef struct LinkedList {
    Node* head;  // Pointer to the head of the list
    int size;    // Size of the list
} LinkedList;

// Function to create a new node
Node* createNode(int coeff, int exp) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->coeff = coeff;
    newNode->exp = exp;
    newNode->next = NULL;
    return newNode;
}

// Function to initialize the linked list (polynomial)
void initList(LinkedList* list) {
    list->head = NULL;
    list->size = 0;
}

// Function to append a term to the polynomial list
void appendTerm(LinkedList* poly, int coeff, int exp) {
    Node* newNode = createNode(coeff, exp);
    if (poly->head == NULL || poly->head->exp < exp) {
        // Insert at the head
        newNode->next = poly->head;
        poly->head = newNode;
    } else {
        Node* temp = poly->head;
        while (temp->next != NULL && temp->next->exp >= exp) {
            temp = temp->next;
        }
        if (temp->exp == exp) {
            // Combine terms with the same exponent
            temp->coeff += coeff;
            free(newNode);  // Don't need the new node if we just combined terms
        } else {
            // Insert the new node
            newNode->next = temp->next;
            temp->next = newNode;
        }
    }
    poly->size++;
}

// Function to display the polynomial
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

// Function to add two polynomials
LinkedList* addPolynomials(LinkedList* poly1, LinkedList* poly2) {
    LinkedList* result = (LinkedList*)malloc(sizeof(LinkedList));
    initList(result);

    Node* p1 = poly1->head;
    Node* p2 = poly2->head;

    while (p1 != NULL && p2 != NULL) {
        if (p1->exp > p2->exp) {
            appendTerm(result, p1->coeff, p1->exp);
            p1 = p1->next;
        } else if (p1->exp < p2->exp) {
            appendTerm(result, p2->coeff, p2->exp);
            p2 = p2->next;
        } else {
            int sum = p1->coeff + p2->coeff;
            if (sum != 0) {
                appendTerm(result, sum, p1->exp);
            }
            p1 = p1->next;
            p2 = p2->next;
        }
    }

    // Append remaining terms
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

    // Example: 5x^3 + 2x
    appendTerm(&poly1, 5, 3);
    appendTerm(&poly1, 2, 1);

    // Example: 3x^2 + 2x
    appendTerm(&poly2, 3, 2);
    appendTerm(&poly2, 2, 1);

    printf("Polynomial 1: ");
    displayPoly(&poly1);

    printf("Polynomial 2: ");
    displayPoly(&poly2);

    LinkedList* result = addPolynomials(&poly1, &poly2);
    printf("Sum: ");
    displayPoly(result);

    // Free allocated memory
    // TODO: Implement free functions for nodes and lists

    return 0;
}
