import os
import random
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
        # From a given address, we compute its corresponding block idx
        incoming_block = addr % self.bucket_size
        # this is our initial target block
        target_block_idx = incoming_block
        print(position)
        # The position map needs to be updated
        new_position = self.updatePostitionMap(addr, position)
        print(new_position)
        
        # get the bucket to read
        bucket = self.getBucket(position)
        
        # for every block in the bucket, we have to generate reads. This is an
        # expensive process
        # we need to return data is the command is a read request
        access_data = None
        for idx, block in enumerate(bucket):
            # our target block is in one onf these blocks
            if target_block_idx == idx:
                if cmd == "R":
                    access_data = block
                else:
                    bucket[idx] = data
        
        # TODO: Remapping code should be here.
        # now write this block to the tree at the new position
        self.writeBucket(new_position, bucket)
        
        return access_data
        # Get the path of the above eaddr
    
    def writeBucket(self, new_position, bucket):
        # FIXME: This is not 100% correct
        cur_pos = self.tree.root
        flag = False
        for pos in new_position:
            if pos == -1:
                cur_pos = cur_pos.left
            elif pos == 1:
                cur_pos = cur_pos.right
            else:
                # we write here
                cur_pos.value = bucket
                flag = True
                break
        return flag
    
    def getBucket(self, position):
        cur_pos = self.tree.root
        bucket = []
        for pos in position:
            if pos == -1:
                cur_pos = cur_pos.left
            elif pos == 1:
                cur_pos = cur_pos.right
            else:
                # found the bucket
                bucket = cur_pos.value
                break
        if len(bucket) == 0:
            print("fatal: position not found")
            exit(-1)
        return bucket
    
    def initializePositionMap(self):
        # Every index needs to have an root
        self._idxMap = {}
        self._posMap = {}
        self._isEmptyLocation = []
        for address in range(0, self.bucket_size * (2 ** self.L - 1)):
            self._idxMap[address] = address
            self._posMap[address] = [0 for _ in range(self.L)]
            self._isEmptyLocation.append(True)
    
    def updatePostitionMap(self, addr, old_position):
        # now, assign a new position for addr
        new_addr = random.randint(0, self.bucket_size * (2 ** self.L - 1))
        flag_check = self._isEmptyLocation[new_addr]
        if flag_check == True:
            # This is a free spot. We do not need to swap
            self._isEmptyLocation[new_addr] = False
            self._idxMap[addr] = new_addr
        else:
            # This location is taken. We need to swap two positions
            old_addr = self._idxMap[new_addr]
            self._idxMap[new_addr] = self._idxMap[addr]
            self._idxMap[addr] = old_addr
        self._posMap[new_addr] = [random.randint(-1,1) for _ in range(self.L)]
        return self._posMap[new_addr]

    def getPosition(self, addr):
        # First find where is the index
        location = self._idxMap[addr]
        # Now get the position from the location
        position = self._posMap[location]
        return position
        