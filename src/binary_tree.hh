// Code for a binary tree. Generated using AI/internet
#ifndef BINARY_TREE_HH
#define BINARY_TREE_HH
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <map>
#include <cassert>

// TODO: Add namespaces to make this code better!

extern int current_node_index;
extern int map_index;
extern std::map<int, std::vector<int>>position_map;

struct BTNode {
    int node_idx;
    int *data;             // This is an array of buckets
    struct BTNode *left;
    struct BTNode *right;
};

struct BTNode* createNode(int bucket_size);

// For remapping, a path and a target node is given to swap
bool swapNodes(struct BTNode* root, int node_idx, std::vector<int> path);

// This function should automatically fillup the tree.
void fillTree(struct BTNode *node, int bucket_size, int depth);

// A function to do DFS.
void betterDfs(struct BTNode* node, std::vector<int>path, int pathLen);

#endif

