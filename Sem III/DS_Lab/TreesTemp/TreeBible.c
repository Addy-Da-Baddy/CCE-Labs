// Online C compiler to run C program online
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct node{
    int data;
    struct node* rlink;
    struct node* llink;
}node;

node* createNode(int data){
    node* newNode = (node*)malloc(sizeof(node));
    newNode->data = data;
    newNode->rlink = NULL;
    newNode->llink = NULL;
    return newNode;
}

node* search(node* root, int val) {
    if (root == NULL) {
        return NULL;  // Value not found
    }
    if (root->data == val) {
        return root;  // Value found, return the node
    }

    // Recursively search in the left and right subtrees
    node* foundNode = search(root->llink, val);
    if (foundNode != NULL) {
        return foundNode;  // If found in the left subtree, return the node
    }

    return search(root->rlink, val);  // Otherwise, search in the right subtree
}


node* createTree(){
    printf("Enter a node. Press -1 to exit creation: ");
    int data;
    scanf("%d" , &data);
    if (data==-1)
        return NULL;
    node* newNode = createNode(data);
    newNode->llink = createTree();
    newNode->rlink = createTree();
    return newNode;
}

void inOrder(node* root){
    if (root==NULL)
        return ;
    inOrder(root->llink);
    printf("%d " , root->data);
    inOrder(root->rlink);
}

void preOrder(node* root){
    if (root==NULL)
        return ;
    printf("%d " , root->data);
    preOrder(root->llink);

    preOrder(root->rlink);
}


void postOrder(node* root){
    if (root==NULL)
        return ;
    postOrder(root->llink);
    postOrder(root->rlink);
    printf("%d " , root->data);
}

bool search(node* root, int val){
    if (root == NULL){
        return false;
    }
    if (root->data == val )
        return true;
    return search(root->rlink,val) || search(root->llink, val) ;
}

int countLeafs(node* root){
    if (root==NULL)
        return 0;
    if (root->llink == NULL && root->rlink == NULL)
        return 1;
    return countLeafs(root->llink) + countLeafs(root->rlink);
}


int findHeight(node* root){
    if (root==NULL)
        return 0;
    int left = findHeight(root->llink);
    int right = findHeight(root->rlink);
    return (left>right? left : right) + 1;
}

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

node* printAncestors(node* root, int target){
    node* parent = findParent(root, target);
    while (parent != NULL) {
        printf("%d ", parent->data);
        parent = findParent(root, parent->data);  // Find the parent of the current parent
    }
}


node* copyTree(node* root){
    if (root==NULL)
        return NULL;
    node* newRoot = createNode(root->data);
    newRoot->llink = copyTree(root->llink);
    newRoot->rlink = copyTree(root->rlink);
    return newRoot;
}


node* mirrorTree(node* root){
    if (root==NULL)
        return NULL;
    node* newRoot = createNode(root->data);
    newRoot->rlink = mirrorTree(root->llink);
    newRoot->llink = mirrorTree(root->rlink);
    return newRoot;
}


int areTreesEqual(node* tree1, node* tree2) {
    if (tree1 == NULL && tree2 == NULL) {
        return 1;
    }
    if (tree1 == NULL || tree2 == NULL) {
        return 0;
    }
    return (tree1->data == tree2->data) &&
           areTreesEqual(tree1->llink, tree2->llink) &&
           areTreesEqual(tree1->rlink, tree2->rlink);
}

int areTreesMirror(node* tree1, node* tree2) {
    if (tree1 == NULL && tree2 == NULL) {
        return 1;
    }
    if (tree1 == NULL || tree2 == NULL) {
        return 0;
    }
    return (tree1->data == tree2->data) &&
           areTreesMirror(tree1->llink, tree2->rlink) &&
           areTreesMirror(tree1->rlink, tree2->llink);
}


int findDepth(node* root, node* target) {
    if (root == NULL)
        return -1;  // Target not found in the tree

    // Base case: if root is the target node, depth is 0
    if (root == target)
        return 0;

    // Check the left and right subtrees for the target node
    int leftDepth = findDepth(root->llink, target);
    int rightDepth = findDepth(root->rlink, target);

    // If the node was found in the left or right subtree, add 1 to the depth
    if (leftDepth != -1)
        return leftDepth + 1;
    else if (rightDepth != -1)
        return rightDepth + 1;

    // If the target node is not found in either subtree, return -1
    return -1;
}


int findHeight(node* target) {
    if (target == NULL)
        return -1;  // Height of an empty subtree is -1

    int leftHeight = findHeight(target->llink);
    int rightHeight = findHeight(target->rlink);

    return (leftHeight > rightHeight ? leftHeight : rightHeight) + 1;
}

int findDepth(node* root, int targetValue) {
    node* targetNode = search(root, targetValue);  // Search for the node
    if (targetNode == NULL)
        return -1;  // Node not found in the tree

    // If the node is the root itself, its depth is 0
    if (root == targetNode)
        return 0;

    // Otherwise, calculate the depth by searching the tree
    int leftDepth = findDepth(root->llink, targetValue);
    int rightDepth = findDepth(root->rlink, targetValue);

    // If the node is found in either subtree, return the depth
    if (leftDepth != -1)
        return leftDepth + 1;
    if (rightDepth != -1)
        return rightDepth + 1;

    return -1;  // Target node not found
}

// Function to find the height of a node (given its value)
int findHeightNode(node* root, int targetValue) {
    node* targetNode = search(root, targetValue);  // Search for the node
    if (targetNode == NULL)
        return -1;  // Node not found in the tree

    // If the node is NULL, height is -1 (base case)
    if (targetNode == NULL)
        return -1;

    // Calculate the height of the left and right subtrees
    int leftHeight = findHeight(targetNode->llink, targetValue);
    int rightHeight = findHeight(targetNode->rlink, targetValue);

    // Height of the node is the maximum height of its subtrees + 1
    if (leftHeight > rightHeight)
        return leftHeight + 1;
    else
        return rightHeight + 1;
}


int main(){
    node* root1 = createTree();
    printf("Inorder: ");
    inOrder(root1);
    printf("\n");
    printf("Preorder: ");
    preOrder(root1);
    printf("\n");
    printf("Postorder: ");
    postOrder(root1);
    int found = search(root1,3);
    printf("\n");
    if (found)
        printf("Found");
    else 
        printf("Nope");
        
    printf ("\n Number of Leafs: %d \n", countLeafs(root1));
    
    printf("Height: %d \n " , findHeight(root1));
    
    printf("Parent of 5 is %d \n", findParent(root1,5)->data);
    
    printf("Ancestors of 5 is: ");
    printAncestors(root1,5);
    printf("\n");
    
    node* root2 = copyTree(root1);
    printf("Preorder: ");
    preOrder(root2);
    printf("\n");
    
    node* root3 = mirrorTree(root1);
    printf("Preorder: ");
    preOrder(root3);
    printf("\n");
    
    printf("%d \n ", areTreesMirror(root1,root3));
    printf("%d \n ", areTreesMirror(root1,root2));
    printf("%d \n ", areTreesEqual(root1,root2));
    printf("%d \n ", areTreesEqual(root1,root3));
    
}
