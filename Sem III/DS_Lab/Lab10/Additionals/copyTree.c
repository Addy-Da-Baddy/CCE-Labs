#include <stdio.h>
#include <stdlib.h>

typedef struct tnode {
    struct tnode* llink;
    struct tnode* rlink;
    int data;
} tnode;

tnode* createNode(int value) {
    tnode* newNode = (tnode*)malloc(sizeof(tnode));
    newNode->data = value;
    newNode->llink = NULL;
    newNode->rlink = NULL;
    return newNode;
}

tnode* copyTree(tnode* root) {
    if (root == NULL) {
        return NULL;
    }
    tnode* newNode = createNode(root->data);
    newNode->llink = copyTree(root->llink);
    newNode->rlink = copyTree(root->rlink);
    return newNode;
}

void printTree(tnode* root) {
    if (root == NULL) {
        return;
    }
    printTree(root->llink);
    printf("%d ", root->data);
    printTree(root->rlink);
}

tnode* insertNode(tnode* root, int value) {
    if (root == NULL) {
        return createNode(value);
    }
    if (value < root->data) {
        root->llink = insertNode(root->llink, value);
    } else {
        root->rlink = insertNode(root->rlink, value);
    }
    return root;
}

int main() {
    tnode* originalTree = NULL;
    int n, value;

    printf("Enter number of nodes for the original tree: ");
    scanf("%d", &n);
    printf("Enter values for the original tree: ");
    for (int i = 0; i < n; i++) {
        scanf("%d", &value);
        originalTree = insertNode(originalTree, value);
    }

    tnode* copiedTree = copyTree(originalTree);

    printf("In-Order Traversal of Original Tree: ");
    printTree(originalTree);
    printf("\n");

    printf("In-Order Traversal of Copied Tree: ");
    printTree(copiedTree);
    printf("\n");

    return 0;
}

