import binary_tree
from queue import Queue
import os

def generate_random_data(byte_size):
    return os.urandom(byte_size)

class p_oram:
    def __init__(self, L = 3, Z = 1, C = 8, B=8):
        default_bucket = [{"valid": 0, "dummy": 0, "block_num":0, "RAM_address":0}]

        #Initialize binary tree
        self.btree = binary_tree.BinaryTree(default_bucket)
        self.btree.root = self.btree.create_full_binary_tree(L+1, default_bucket)

        #Initialize Pos Map
        self.pos_map = {} #key is block_num and value is node ID of leaf

        #Initialize Stash
        self.stash = []

        self.Block_byte_size = B

    def print_btree(self):
        self.btree.inorder_traversal(self.btree.root)

    def ORAM_access(self, block_num):
        #Client provides block_num for required data block (in RAM)

        #Use Pos Map to determine leaf / path to check
        leaf_id = self.pos_map[block_num]
        self.btree.find_paths_to_leaves
        leaf_path = self.btree.leaf_paths[leaf_id]

        #Pop entire path from Binary tree and store in stash
        self.stash_populate(leaf_path)

        #Retrieve bucket / block of interest and get RAM address
        for block in self.stash:
            if((block['block_num'] == block_num) and (block["valid"])):
                client_block = block
        
        #Retrieve data from ORAM using actual address
        block_data = generate_random_data(self.Block_byte_size)
        #Return data to client
        return block_data

    def stash_populate(self, path):
        node = self.btree.root
        for i in path:
            if(node.data["vaid"]):
                self.stash.append(node.data)
            if(i):
                node = node.right
            else:
                node = node.left

    def periodic_stash_eviction(self):
        return ""





# Example usage
if __name__ == '__main__':
 poram_instance = p_oram()
 poram_instance.__print_btree__()


