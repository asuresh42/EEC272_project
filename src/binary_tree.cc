#include "binary_tree.hh"

// We need a bunch of global variables to make this work
int current_node_index = 0;
int path_index = 0;
std::map<int, std::vector<int>>position_map;

struct BTNode* createNode(int bucket_size) {
    struct BTNode *node = (struct BTNode*)malloc(sizeof(struct BTNode));
    node->node_idx = current_node_index++;
    node->data = (int *)malloc(bucket_size * sizeof(int));
    // Set all the entries in the block to 0
    for(int i = 0 ; i < bucket_size ; i++)
        node->data[i] = 0;
    node->left = NULL;
    node->right = NULL;
    return node;
}

// This function should automatically fillup the tree.
void fillTree(struct BTNode *node, int bucket_size, int depth) {
    if (depth > 0) {
        node->left = createNode(bucket_size);
        node->right = createNode(bucket_size);
        fillTree(node->left, bucket_size, depth - 1);
        fillTree(node->right, bucket_size, depth - 1);
    }
    else
        return;
}

// This function performs DFS
void betterDfs(struct BTNode* node, std::vector<int> path, int pathLen) {
        if (node == NULL) {
        return;
    }

    path[pathLen] = node->node_idx;
    pathLen++;

    if (node->left == NULL && node->right == NULL) {
        // This is a leaf node. Add this to the path table.
        position_map[path_index++] = path;

        // printf("Path length %d: ", pathLen);
        // for (int i = 0; i < pathLen; i++) {
        //     printf("%d ", path[i]);
            // printf("-- %d . %d ", path_index - 1, position_map[path_index -  1][i]);
        // }
        // printf("\n");
    } else {
        betterDfs(node->left, path, pathLen);
        betterDfs(node->right, path, pathLen);
    }
}