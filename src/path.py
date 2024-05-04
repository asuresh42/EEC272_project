import os
import random
from src.binary_tree import BinaryTree, Node

class Stash:
    def __init__(self, addr, position):
        self.addr = addr
        self.position = position

class PathORAM:
    """This class creates an ORAM structure without recursion
        :params:
        block_size : Block size of the ORAM
        bucket size : Size of the leaf bucket
    """
    def __init__(self, block_size = 64, bucket_size = 4):
        self.block_size = block_size
        self.bucket_size = bucket_size
        self.L = 3
        self.stash = []     # inf stash
        # size of the dram device in bits
        self.size_of_dram = self.block_size * self.bucket_size * (2 ** self.L  - 1)
        self.real_blocks = 0
        self.dummy_blocks = self.bucket_size * (2 ** self.L  - 1)
        self.initializeTree()
        
    def printSize(self):
        return self.size_of_dram
        
    def initializeTree(self):
        # setup the binary tree. The tree structure does not change. Initially
        # all the entries of the tree is filled up with zeros. This map can be
        # statically initialized for now.
        
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
        
        self.initializePositionMapV2()
        
    #def getAddr(self, block, position):
    def accessAddr(self, addr, cmd, data = None):
        """This is the base method that the user needs to use to access a
        location in the ORAM structure.

        Args:
            addr (int): Address
            cmd (char) ['R' or 'W']
            data (int): If this is a write request, then there is data
                        associated with this address
        """
        ########################## Trusted ####################################
        
        # Get the effective address for the given addr
        position = self.getPosition(addr)

        # From a given address, we compute its corresponding block idx (in one node which bucket)
        incoming_bucket_idx = addr % self.bucket_size
        # this is our initial target block
        target_block_idx = incoming_bucket_idx
        print(position)
        # The position map needs to be updated
        new_position = self.updatePostitionMapV2(addr, position)
        print(new_position)
        
        # Now check if we have this address in the stash. We'll discard the
        # position that we retrived with the already updated position
        idx_to_delete = -1
        for idx in range(len(self.stash)):
            print(self.stash.addr)
            if self.stash[idx].addr == addr:
                # position = stash.position
                idx_to_delete = idx
                break
        
        # if idx_to_delete != -1:
        #     # found this address in the stash!
        #     # FIXME:
        #     target_block_idx = -1
        # get the bucket to read
        buckets = self.getBucketV2(position)
        
        for bucket in buckets:
            new_stash = Stash(addr, position)
            self.stash.append(new_stash)           # S = S U bucket
        
        # for every block in the bucket, we have to generate reads. This is an
        # expensive process
        # we need to return data is the command is a read request
        access_data = None
        
        ########################## Trusted End ################################
        
        # Need to access every block from every bucket to make the number of
        # reads consistent.
        for idx, bucket in enumerate(buckets):
            for jdx, block in enumerate(bucket):
                # We read all of these blocks
                # idx gives the level and jdx gives the block
                this_addr = (idx + 1) * self.block_size  
                if target_block_idx == idx:
                    # This is a valid block
                    self.stash.append(Stash(addr, new_position))
                    if cmd == "R":
                        access_data = block
                    else:
                        bucket[idx] = data
                        self.real_blocks += 1
                        self.dummy_blocks -= 1
        
        # TODO: Remapping code should be here.
        # now write this block to the tree at the new position
        # Now, search the stash if we have things to write back to this
        # position we have.
        self.writeBucket(new_position, bucket)
        
        ########################## Trusted ####################################
        
        return access_data
        
        ########################## Trusted End ################################
    
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
    
    def getBucketV2(self, position):
        # return all buckets in this path
        buckets = []
        cur_pos = self.tree.root
        for pos in position:
            buckets.append(cur_pos.value)
            if pos == 0:
                cur_pos = cur_pos.left
            elif pos == 1:
                cur_pos = cur_pos.right
        if len(buckets) == 0:
            print("fatal: position not found")
            exit(-1)
        return buckets
    
    def initializePositionMapV2(self):
        # Every index needs to have an root
        self._idxMap = {}
        self._posMap = {}
        self._isEmptyLocation = []
        for address in range(0, self.bucket_size * (2 ** self.L - 1)):
            self._idxMap[address] = address
            # So the binary string of the position is the path as a direction
            pos = bin(random.randint(0, 2 ** (self.L - 1)))
            self._posMap[address] = []
            for bins in str(pos)[2:]:
                self._posMap[address].append(int(bins))
            if len(self._posMap[address]) == 1:
                self._posMap[address].append(0)
            self._isEmptyLocation.append(True)
    
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
    
    def updatePostitionMapV2(self, addr, old_position):
        pos = bin(random.randint(0, 2 ** (self.L - 1)))
        self._posMap[addr] = []
        for bins in str(pos)[2:]:
            self._posMap[addr].append(int(bins))
        if len(self._posMap[addr]) == 1:
            self._posMap[addr].append(0)
        return self._posMap[addr]

    def getPosition(self, addr):
        # First find where is the index
        location = self._idxMap[addr]
        # Now get the position from the location
        position = self._posMap[location]
        return position
        