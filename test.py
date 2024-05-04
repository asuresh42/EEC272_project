import random
from src.binary_tree import BinaryTree, Node
from src.path import PathORAM
tree = BinaryTree(1)
tree.root.left = Node(2)
tree.root.right = Node(3)
tree.root.left.left = Node(4)
tree.root.left.right = Node(5)

print(tree.print_tree("preorder"))  # 1-2-4-5-3-

X = PathORAM()

bit_max = 2**64 - 1

print(X.printSize()/8/1024, "KiB")

# data is a 64 bit block -> 8 bytes -> address and access granuality at block level, block address passed to accessAddr

print(X.accessAddr(0xa, cmd = "R"))
# send a write request first
print(X.accessAddr(14, cmd = "W", data = (random.randrange(0, bit_max)) ),"\n")
print(X.accessAddr(3, cmd = "W", data = [1 for i in range(64)]),"\n")
print(X.accessAddr(5, cmd = "W", data = [1 for i in range(64)]),"\n")
print(X.accessAddr(1, cmd = "W", data = [1 for i in range(64)]),"\n")
print(X.accessAddr(11, cmd = "W", data = [1 for i in range(64)]),"\n")

# read the previous block
print(X.accessAddr(0xa, cmd = "R"))

test_client_DRAM = {}       # DRAM simulated as a dictionary with key<->value as addr<->data_value

for i in range(21):        # 5 nodes, each with 4 blocks, 20 total blocks, each block is 8 bytes, so a total of 160 bytes in client_DRAM
    key = i
    value = random.randrange(0,255)
    test_client_DRAM[key] = value

print(test_client_DRAM)     

# write client DRAM onto server
for j in range(20):
    print(X.accessAddr(j, cmd = "W", data = [random.randrange(0,2) for i in range(64)]))

