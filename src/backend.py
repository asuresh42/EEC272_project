import os
from src.binary_tree import BinaryTree, Node


class PathORAM:
    """This class creates an ORAM structure without recursion
        :params:
        block_size : Block size of the ORAM
        bucket size : Size of the leaf bucket
    """
    def __init__(self, block_size = 64, bucket_size = 1024):
        self.block_size = block_size
        self.bucket_size = bucket_size
        self.L = 3
        # size of the dram device in bits
        self.size_of_dram = self.block_size * self.bucket_size * (2 ** self.L  - 1)
        self.initializeTree()
        
    def printSize(self):
        return self.size_of_dram
        
    def initializeTree(self):
        # setup the binary tree. The tree structure does not change. Initially
        # all the entries of the tree is filled up with zeros
        self.tree = BinaryTree([[0 for _ in range(self.block_size)] for _ in range(self.bucket_size)])
        # for i in range(0, 2 ** self.L  - 1):
        self.tree.root.left = Node([[0 for _ in range(self.block_size)] for _ in range(self.bucket_size)])
        self.tree.root.right = Node([[0 for _ in range(self.block_size)] for _ in range(self.bucket_size)])
        
        self.tree.root.left.left = Node([[0 for _ in range(self.block_size)] for _ in range(self.bucket_size)])
        self.tree.root.left.right = Node([[0 for _ in range(self.block_size)] for _ in range(self.bucket_size)])
        self.tree.root.right.left = Node([[0 for _ in range(self.block_size)] for _ in range(self.bucket_size)])
        self.tree.root.right.right = Node([[0 for _ in range(self.block_size)] for _ in range(self.bucket_size)])
        
        # TODO: Make this automated
        # TODO: We need a AVL
        
        self.initializePositionMap()
    
    def accessAddr(self, addr, cmd, data = None):
        """This is the base method that the user needs to use to access a
        location in the ORAM structure.

        Args:
            addr (int): Address
            cmd (char) ['R' or 'W']
            data (int): If this is a write request, then there is data
                        associated with this address
        """
        # Get the effective address for the given addr
        position = self.getPosition(addr)
        print(position)
        # The position map needs to be updated
        # self.updatePostitionMap(addr)
        
        # Get the path of the above eaddr
    
    def initializePositionMap(self):
        # Every index needs to have an root
        self._idxMap = {}
        self._posMap = {}
        self._isEmptyLocation = []
        for address in range(0, self.bucket_size * (2 ** self.L - 1)):
            self._idxMap[address] = address
            self._posMap[address] = [0 for _ in range(self.L)]
            self._isEmptyLocation.append(True)
    
    def updatePostitionMap(self, addr):
        # now, assign a new position for addr
        # check is there is a free location in the first place
        # FIXME: This should be swappable
        flag = False
        for i in range(self.bucket_size * (2 ** self.L - 1)):
            if self._isEmptyLocation[i] == True:
                flag = True
                break
        if flag == False:
            # ran out of memomry!
            print("fatal: no new free space left")
            exit()
        new_location = False
        while new_location == False:
            new_location = self._isEmptyLocation[random.randint(
                                    0, self.bucket_size * (2 ** self.L - 1))]

    def getPosition(self, addr):
        # First find where is the index
        location = self._idxMap[addr]
        # Now get the position from the location
        position = self._posMap[location]
        return position
        