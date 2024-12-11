#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    int data;
    struct node *llink, *rlink;
    int lthread, rthread; // Threads: 1 for thread, 0 for child pointer
} node;

// Function to find the inorder successor in a threaded binary tree
node *in_suc(node *ptr) {
    if (ptr->rthread) { // If right link is a thread, return rlink as successor
        return ptr->rlink;
    }

    // Otherwise, go to the leftmost node in the right subtree
    node *temp = ptr->rlink;
    while (!temp->lthread) {
        temp = temp->llink;
    }
    return temp;
}

// Function to traverse a threaded binary tree in inorder
void tinorder(node *head) {
    if (!head) return; // Handle empty tree

    // Find the leftmost node to start traversal
    node *temp = head;
    while (!temp->lthread) {
        temp = temp->llink;
    }

    // Perform inorder traversal until we return to the head
    while (temp != head) {
        printf("%d ", temp->data);
        temp = in_suc(temp);
    }
}



#include <stdio.h>
#include <stdlib.h>

// Definition of a binary tree node
typedef struct node {
    int data;
    struct node *left, *right;
} node;

// Function to create a new node
node* createNode(int data) {
    node* newNode = (node*)malloc(sizeof(node));
    newNode->data = data;
    newNode->left = newNode->right = NULL;
    return newNode;
}

// Morris Traversal for inorder traversal
void morrisTraversal(node* root) {
    node* current = root;

    while (current != NULL) {
        if (current->left == NULL) {
            // No left child, print the current node and move to the right
            printf("%d ", current->data);
            current = current->right;
        } else {
            // Find the inorder predecessor of current
            node* predecessor = current->left;
            while (predecessor->right != NULL && predecessor->right != current) {
                predecessor = predecessor->right;
            }

            if (predecessor->right == NULL) {
                // Create a thread to the current node
                predecessor->right = current;
                current = current->left;
            } else {
                // Thread exists, remove it and process the current node
                predecessor->right = NULL;
                printf("%d ", current->data);
                current = current->right;
            }
        }
    }
}

