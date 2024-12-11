#include <stdio.h>
#include <stdlib.h>

typedef struct tnode {
    struct tnode* llink;
    struct tnode* rlink;
    int data;
} tnode;

typedef struct BinaryTree {
    tnode* root;
} BinaryTree;

tnode* createTree() {
    int value;
    printf("Enter node value (-1 to indicate no node): ");
    scanf("%d", &value);

    if (value == -1) {
        return NULL;
    }

    tnode* newNode = (tnode*)malloc(sizeof(tnode));
    newNode->data = value;
    newNode->llink = createTree();
    newNode->rlink = createTree();

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

int main() {
    BinaryTree tree;
    printf("Create a binary tree:\n");
    tree.root = createTree();

    printf("In-Order Traversal of the binary tree: ");
    printTree(tree.root);
    printf("\n");

    return 0;
}
