// Code for a binary tree. Generated using AI/internet
#ifndef BINARY_TREE_HH
#define BINARY_TREE_HH
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <map>

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

// This function should automatically fillup the tree.
void fillTree(struct BTNode *node, int bucket_size, int depth);

// A function to do DFS.
void betterDfs(struct BTNode* node, std::vector<int>path, int pathLen);

#endif

