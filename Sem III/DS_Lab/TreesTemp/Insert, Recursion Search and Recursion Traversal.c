#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* llink;
    struct Node* rlink;
} Node;

typedef struct Tree {
    Node* root;
    int size;
} Tree;

// Function to create a new node
Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->data = data;
    newNode->llink = NULL;
    newNode->rlink = NULL;
    return newNode;
}

// Function to initialize the tree
void initializeTree(Tree* tree) {
    tree->root = NULL;
    tree->size = 0;
}

// Function to insert a node based on direction vector
void insertNode(Tree* tree, int data, const char* direction) {
    if (tree->root == NULL) {
        tree->root = createNode(data);
        tree->size++;
        return;
    }

    Node* current = tree->root;
    for (int i = 0; direction[i] != '\0'; i++) {
        if (direction[i] == 'l') {
            if (current->llink == NULL) {
                current->llink = createNode(0);
            }
            current = current->llink;
        } else if (direction[i] == 'r') {
            if (current->rlink == NULL) {
                current->rlink = createNode(0);
            }
            current = current->rlink;
        } else {
            printf("Invalid direction: %c\n", direction[i]);
            return;
        }
    }

    current->data = data;
    tree->size++;
}

// Recursive inorder traversal
void inorder(Node* root) {
    if (root == NULL) return;
    inorder(root->llink);
    printf("%d ", root->data);
    inorder(root->rlink);
}

// Recursive preorder traversal
void preorder(Node* root) {
    if (root == NULL) return;
    printf("%d ", root->data);
    preorder(root->llink);
    preorder(root->rlink);
}

// Recursive search function
int search(Node* root, int value) {
    if (root == NULL) return 0; // Not found
    if (root->data == value) return 1; // Found

    // Search in left and right subtrees
    return search(root->llink, value) || search(root->rlink, value);
}


// Recursive postorder traversal
void postorder(Node* root) {
    if (root == NULL) return;
    postorder(root->llink);
    postorder(root->rlink);
    printf("%d ", root->data);
}

// Example usage
int main() {
    Tree tree;
    initializeTree(&tree);

    insertNode(&tree, 1, "");    // Root
    insertNode(&tree, 2, "l");   // Left of root
    insertNode(&tree, 3, "r");   // Right of root
    insertNode(&tree, 4, "ll");  // Left of left child
    insertNode(&tree, 5, "lr");  // Right of left child
    insertNode(&tree, 6, "rl");  // Left of right child
    insertNode(&tree, 7, "rr");  // Right of right child
    insertNode(&tree, 8, "lll"); // Left of left's left child
    insertNode(&tree, 9, "llr"); // Right of left's left child
    insertNode(&tree, 10, "lrl"); // Left of left's right child
 // Right of root

    printf("Inorder traversal: ");
    inorder(tree.root);
    printf("\n");

    printf("Preorder traversal: ");
    preorder(tree.root);
    printf("\n");

    printf("Postorder traversal: ");
    postorder(tree.root);
    printf("\n");

    return 0;
}
