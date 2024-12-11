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

int areMirrorImages(tnode* tree1, tnode* tree2) {
    if (tree1 == NULL && tree2 == NULL) {
        return 1;
    }
    if (tree1 == NULL || tree2 == NULL) {
        return 0;
    }
    return (tree1->data == tree2->data) &&
           areMirrorImages(tree1->llink, tree2->rlink) &&
           areMirrorImages(tree1->rlink, tree2->llink);
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
    tnode* tree1 = NULL;
    tnode* tree2 = NULL;

    int n1, n2, value;

    printf("Enter number of nodes for Tree 1: ");
    scanf("%d", &n1);
    printf("Enter values for Tree 1: ");
    for (int i = 0; i < n1; i++) {
        scanf("%d", &value);
        tree1 = insertNode(tree1, value);
    }

    printf("Enter number of nodes for Tree 2: ");
    scanf("%d", &n2);
    printf("Enter values for Tree 2: ");
    for (int i = 0; i < n2; i++) {
        scanf("%d", &value);
        tree2 = insertNode(tree2, value);
    }

    if (areMirrorImages(tree1, tree2)) {
        printf("Tree 1 and Tree 2 are mirror images.\n");
    } else {
        printf("Tree 1 and Tree 2 are not mirror images.\n");
    }

    printf("In-Order Traversal of Tree 1: ");
    printTree(tree1);
    printf("\n");

    printf("In-Order Traversal of Tree 2: ");
    printTree(tree2);
    printf("\n");

    return 0;
}
