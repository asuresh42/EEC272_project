class TreeNode:
    _id_counter = 0  # Class variable to keep track of the last used ID

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.node_id = TreeNode._get_next_id()  # Assign a unique ID to each node

    @classmethod
    def _get_next_id(cls):
        """Generates a unique ID."""
        cls._id_counter += 1
        return cls._id_counter

class BinaryTree:
    def __init__(self, root_data):
        self.root = TreeNode(root_data)  # Initialize root with unique ID
        self.leaf_paths = {}  # Dictionary to hold paths to each leaf

    def insert_left(self, current_node, data):
        if current_node.left is None:
            current_node.left = TreeNode(data)
        else:
            new_node = TreeNode(data)
            new_node.left = current_node.left
            current_node.left = new_node

    def insert_right(self, current_node, data):
        if current_node.right is None:
            current_node.right = TreeNode(data)
        else:
            new_node = TreeNode(data)
            new_node.right = current_node.right
            current_node.right = new_node

    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(f'Node ID: {node.node_id}, Data: {node.data}')
            self.inorder_traversal(node.right)

    def create_full_binary_tree(self, depth, default_data):
        if depth < 1:
            return None
        return self._create_full_binary_tree_helper(depth, default_data)

    def _create_full_binary_tree_helper(self, depth, default_data):
        if depth == 0:
            return None
        node = TreeNode(default_data)
        node.left = self._create_full_binary_tree_helper(depth - 1, default_data)
        node.right = self._create_full_binary_tree_helper(depth - 1, default_data)
        return node

    def find_paths_to_leaves(self):
        self.leaf_paths = {}
        self._find_paths_to_leaves_helper(self.root, [])

    def _find_paths_to_leaves_helper(self, node, path):
        if node is None:
            return
        # Traverse to the left child
        if node.left is not None:
            self._find_paths_to_leaves_helper(node.left, path + [0])
        # Traverse to the right child
        if node.right is not None:
            self._find_paths_to_leaves_helper(node.right, path + [1])
        # Check if it's a leaf node
        if node.left is None and node.right is None:
            self.leaf_paths[node.node_id] = path

# Example usage
if __name__ == '__main__':
    default_value = 0
    tree_depth = 3  # Depth of the full binary tree

    btree = BinaryTree(default_value)
    btree.root = btree.create_full_binary_tree(tree_depth, default_value)

    # Calculate paths to all leaves
    btree.find_paths_to_leaves()

    # Print all nodes in the tree in in-order traversal
    btree.inorder_traversal(btree.root)

    # Print paths to all leaf nodes
    print("Paths to leaves:")
    for leaf_id, path in btree.leaf_paths.items():
        print(f'Leaf Node ID: {leaf_id}, Path: {path}')
