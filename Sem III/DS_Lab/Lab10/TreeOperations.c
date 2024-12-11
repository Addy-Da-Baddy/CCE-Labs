#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#define MAXSIZE 100

typedef struct tnode {
    struct tnode* llink;
    struct tnode* rlink;
    int data;
} tnode;

typedef struct BinaryTree {
    tnode* root;
} BT;

typedef struct stack {
    int top;
    tnode* items[MAXSIZE];
} stack;

// Stack functions
void initStack(stack* s) {
    s->top = -1;
}

void push(stack* s, tnode* node) {
    if (s->top < MAXSIZE - 1) {
        s->items[++s->top] = node;
    }
}

tnode* pop(stack* s) {
    if (s->top > -1) {
        return s->items[s->top--];
    }
    return NULL;
}

// Tree traversal functions
void inOrder(BT* tree) {
    stack s;
    initStack(&s);
    tnode* curr = tree->root;
    while (curr != NULL || s.top != -1) {
        while (curr != NULL) {
            push(&s, curr);
            curr = curr->llink;
        }
        curr = pop(&s);
        printf("%d ", curr->data);
        curr = curr->rlink;
    }
}

void preOrder(BT* tree) {
    stack s;
    initStack(&s);
    push(&s, tree->root);
    while (s.top != -1) {
        tnode* curr = pop(&s);
        printf("%d ", curr->data);
        if (curr->rlink) push(&s, curr->rlink);
        if (curr->llink) push(&s, curr->llink);
    }
}

void postOrder(BT* tree) {
    stack s1, s2;
    initStack(&s1);
    initStack(&s2);
    push(&s1, tree->root);
    while (s1.top != -1) {
        tnode* curr = pop(&s1);
        push(&s2, curr);
        if (curr->llink) push(&s1, curr->llink);
        if (curr->rlink) push(&s1, curr->rlink);
    }
    while (s2.top != -1) {
        tnode* curr = pop(&s2);
        printf("%d ", curr->data);
    }
}

// Insert a new node into the binary tree
tnode* createNode(int data) {
    tnode* newNode = (tnode*)malloc(sizeof(tnode));
    newNode->data = data;
    newNode->llink = NULL;
    newNode->rlink = NULL;
    return newNode;
}

void insertNode(BT* tree, int data) {
    tnode* newNode = createNode(data);
    if (tree->root == NULL) {
        tree->root = newNode;
        return;
    }
    
    // Use a queue for level-order insertion
    stack s;
    initStack(&s);
    push(&s, tree->root);

    while (s.top != -1) {
        tnode* curr = pop(&s);
        if (curr->llink == NULL) {
            curr->llink = newNode;
            return;
        } else {
            push(&s, curr->llink);
        }
        if (curr->rlink == NULL) {
            curr->rlink = newNode;
            return;
        } else {
            push(&s, curr->rlink);
        }
    }
}

// Find parent of a node
node* findParent(node* root, int target) {
    // Base case: if root is NULL or the root itself is the target
    if (root == NULL || root->data == target) {
        return NULL;
    }

    // Check if either the left or right child is the target node
    if ((root->llink != NULL && root->llink->data == target) || 
        (root->rlink != NULL && root->rlink->data == target)) {
        return root;  // Found the parent node
    }

    // Recursively search in the left subtree
    node* leftParent = findParent(root->llink, target);
    if (leftParent != NULL) {
        return leftParent;
    }

    // If not found in left, search in the right subtree
    return findParent(root->rlink, target);
}

// Print ancestors of a node
bool printAncestors(tnode* root, int value) {
    if (root == NULL) {
        return false;
    }
    if (root->data == value) {
        return true;
    }
    if (printAncestors(root->llink, value) || printAncestors(root->rlink, value)) {
        printf("%d ", root->data);
        return true;
    }
    return false;
}

// Count leaf nodes
int countLeaf(tnode* root) {
    if (root == NULL) {
        return 0;
    }
    if (root->llink == NULL && root->rlink == NULL) {
        return 1;
    }
    return countLeaf(root->llink) + countLeaf(root->rlink);
}

// Find depth of tree
int findDepth(tnode* root) {
    if (root == NULL) {
        return 0;
    }
    int left = findDepth(root->llink);
    int right = findDepth(root->rlink);
    return (left > right ? left : right) + 1;
}

// Free the binary tree
void freeTree(tnode* root) {
    if (root != NULL) {
        freeTree(root->llink);
        freeTree(root->rlink);
        free(root);
    }
}

int main() {
    BT tree;
    tree.root = NULL;

    int choice, valueToFind, valueToInsert;

    while (true) {
        printf("\nMenu:\n");
        printf("1. Insert Node\n");
        printf("2. In-Order Traversal\n");
        printf("3. Pre-Order Traversal\n");
        printf("4. Post-Order Traversal\n");
        printf("5. Find Parent of a Node\n");
        printf("6. Print Ancestors of a Node\n");
        printf("7. Count Leaf Nodes\n");
        printf("8. Find Depth of Tree\n");
        printf("9. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to insert: ");
                scanf("%d", &valueToInsert);
                insertNode(&tree, valueToInsert);
                break;
            case 2:
                printf("In-Order Traversal: ");
                inOrder(&tree);
                break;
            case 3:
                printf("Pre-Order Traversal: ");
                preOrder(&tree);
                break;
            case 4:
                printf("Post-Order Traversal: ");
                postOrder(&tree);
                break;
            case 5:
                printf("Enter node value to find its parent: ");
                scanf("%d", &valueToFind);
                tnode* parent = findParent(tree.root, valueToFind, NULL);
                if (parent) {
                    printf("Parent of %d is %d\n", valueToFind, parent->data);
                } else {
                    printf("Node %d does not have a parent or does not exist in the tree.\n", valueToFind);
                }
                break;
            case 6:
                printf("Enter node value to find its ancestors: ");
                scanf("%d", &valueToFind);
                printf("Ancestors of %d: ", valueToFind);
                if (!printAncestors(tree.root, valueToFind)) {
                    printf("No ancestors found or the node does not exist.\n");
                }
                break;
            case 7:
                printf("Number of leaf nodes: %d\n", countLeaf(tree.root));
                break;
            case 8:
                printf("Depth of the tree: %d\n", findDepth(tree.root));
                break;
            case 9:
                freeTree(tree.root);  // Free allocated memory before exit
                return 0;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
}
