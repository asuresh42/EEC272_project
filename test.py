from src.binary_tree import BinaryTree, Node
from src.backend import PathORAM

tree = BinaryTree(1)
tree.root.left = Node(2)
tree.root.right = Node(3)
tree.root.left.left = Node(4)
tree.root.left.right = Node(5)

print(tree.print_tree("preorder"))  # 1-2-4-5-3-

X = PathORAM()

print(X.printSize()/8/1024, "KiB")

# data is a 64 bit block -> 8 bytes

print(X.accessAddr(0x0, cmd = "W", data = [i for i in range(64)]))
print(X.accessAddr(0x0, cmd = "R"))