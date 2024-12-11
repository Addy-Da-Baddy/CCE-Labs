int countNonLeafNodes(tnode* root) {
    if (root == NULL) {
        return 0; // Base case: no nodes in an empty tree
    }
    // Count this node if it has at least one child
    int count = (root->llink != NULL || root->rlink != NULL) ? 1 : 0;
    // Recursively count non-leaf nodes in both subtrees
    return count + countNonLeafNodes(root->llink) + countNonLeafNodes(root->rlink);
}


int countNodesWithTwoChildren(tnode* root) {
    if (root == NULL) {
        return 0; // Base case: no nodes in an empty tree
    }
    // Count this node if it has both children
    int count = (root->llink != NULL && root->rlink != NULL) ? 1 : 0;
    // Recursively count in both subtrees
    return count + countNodesWithTwoChildren(root->llink) + countNodesWithTwoChildren(root->rlink);
}
int countLeafNodes(tnode* root) { 
    if (root == NULL) {
        return 0; // Base case: no nodes in an empty tree
    }
    // Count this node if it is a leaf node (no children)
    if (root->llink == NULL && root->rlink == NULL) {
        return 1; // This is a leaf node
    }
    // Recursively count leaf nodes in both subtrees
    return countLeafNodes(root->llink) + countLeafNodes(root->rlink); 
}
