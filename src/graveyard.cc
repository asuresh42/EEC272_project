// Define the structure for tree node
// struct Node {
//     int data;
//     struct Node* left;
//     struct Node* right;
// };


/*
// This is the DFS function
void dfs(Node* node) {
    if (node == NULL) {
        return;
    }
    printf("%d ", node->value);  // Process the node
    dfs(node->left);  // Recurse on left subtree
    dfs(node->right);  // Recurse on right subtree
}

void better_dfs(Node* node, int path[], int pathLen) {
    if (node == NULL) {
        return;
    }

    path[pathLen] = node->node_idx;
    pathLen++;

    if (node->left == NULL && node->right == NULL) {
        printf("Path %d: ", pathLen);
        for (int i = 0; i < pathLen; i++) {
            printf("%d ", path[i]);
        }
        printf("\n");
    } else {
        dfs(node->left, path, pathLen);
        dfs(node->right, path, pathLen);
    }
}

// Function to create a new node
struct Node* newNode(int data) {
    struct Node* node = (struct Node*)malloc(sizeof(struct Node));
    node->data = data;
    node->left = NULL;
    node->right = NULL;
    return(node);
}

// Function to print the tree in order
void printInOrder(struct Node* node) {
    if (node == NULL)
        return;
    printInOrder(node->left);
    printf("%d ", node->data);
    printInOrder(node->right);
}

// Function to insert a new node with given data
struct Node* insert(struct Node* node, int data) {
    if (node == NULL) 
        return(newNode(data));
    else {
        if (data <= node->data)
            node->left = insert(node->left, data);
        else
            node->right = insert(node->right, data);
        return node;
    }
}
/-
int main() {
    /- Let us create following BST
              50
           /     \
          30      70
         /  \    /  \
       20   40  60   80 -/
    struct Node *root = NULL;
    root = insert(root, 50);
    insert(root, 30);
    insert(root, 20);
    insert(root, 40);
    insert(root, 70);
    insert(root, 60);
    insert(root, 80);

    // print inoder traversal of the BST
    printInOrder(root);

    return 0;
}
*/
