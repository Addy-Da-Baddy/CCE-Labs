#include <stdio.h>
#include <stdbool.h>

typedef struct tnode{
    struct tnode* llink;
    struct tnode* rlink;
    int data;
}tnode;

typedef struct BinaryTree{
    tnode* root;
}BT;

tnode* createNode(int value) {
    tnode* newNode = (tnode*)malloc(sizeof(tnode));
    newNode->data = value;
    newNode->llink = NULL;
    newNode->rlink = NULL;
    return newNode;
}


tnode* insert(tnode* root, int value) {
    // Base case: If root is NULL, create a new node and return it
    if (root == NULL) {
        return createNode(value);
    }

    // If the value already exists, return root without inserting
    if (value == root->data) {
        printf("Value %d already exists in the tree.\n", value);
        return root;
    }

    // Recur down the tree to find the correct position
    if (value < root->data) {
        root->llink = insert(root->llink, value);  // Insert in the left subtree
    } else {
        root->rlink = insert(root->rlink, value);  // Insert in the right subtree
    }

    return root;  // Return the (possibly updated) root
}


tnode* findMin(tnode* root) {
    while (root && root->llink) {
        root = root->llink;
    }
    return root;
}

tnode* delNode(tnode* root, int val) {
    // Case 0: Base case, tree is empty
    if (root == NULL) {
        return root;
    }

    // Traverse the tree to find the node to delete
    if (root->data > val) {
        root->llink = delNode(root->llink, val);  // Go to the left subtree
    } else if (root->data < val) {
        root->rlink = delNode(root->rlink, val);  // Go to the right subtree
    } else {
        // FOUND THE NODE TO DELETE

        // Case 1: No children (leaf node)
        if (root->llink == NULL && root->rlink == NULL) {
            free(root);
            root = NULL;
            return root;
        }
        // Case 2: Only one child (right child)
        else if (root->rlink != NULL && root->llink == NULL) {
            tnode* temp = root;          // Temporarily store the current node
            root = root->rlink;          // Replace the current node with its right child
            free(temp);                  // Free the original node
            return root;
        }
        // Case 3: Only one child (left child)
        else if (root->llink != NULL && root->rlink == NULL) {
            tnode* temp = root;          // Temporarily store the current node
            root = root->llink;          // Replace the current node with its left child
            free(temp);                  // Free the original node
            return root;
        }
        // Case 4: Two children
        else {
            // Find the minimum value in the right subtree
            tnode* min = findMin(root->rlink);
            // Replace the current node's data with the min value from the right subtree
            root->data = min->data;
            // Now, delete the node containing the minimum value from the right subtree
            root->rlink = delNode(root->rlink, min->data);
        }
    }

    return root;
}



tnode* search(tnode* root, int value) {
    if (root == NULL || root->data == value) {
        return root;
    }
    if (value < root->data) {
        return search(root->llink, value);
    }
    return search(root->rlink, value);
}

void printTree(tnode* root) {
    if (root != NULL) {
        printTree(root->llink);
        printf("%d ", root->data);
        printTree(root->rlink);
    }
}


#include <stdio.h>
#include <stdlib.h>

int main() {
    BT tree;
    tree.root = NULL;
    int choice, value;

    while (1) {
        printf("Menu:\n");
        printf("1. Insert\n");
        printf("2. Delete\n");
        printf("3. Search\n");
        printf("4. Print Tree\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to insert: ");
                scanf("%d", &value);
                tree.root = insert(tree.root, value);
                break;
            case 2:
                printf("Enter value to delete: ");
                scanf("%d", &value);
                tree.root = deleteNode(tree.root, value);
                break;
            case 3:
                printf("Enter value to search: ");
                scanf("%d", &value);
                if (search(tree.root, value)) {
                    printf("%d found in the tree.\n", value);
                } else {
                    printf("%d not found in the tree.\n", value);
                }
                break;
            case 4:
                printf("In-order traversal: ");
                printTree(tree.root);
                printf("\n");
                break;
            case 5:
                exit(0);
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
    return 0;
}



