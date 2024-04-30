import binary_tree
from queue import Queue
import os
import random

def generate_random_data(byte_size): #generate_random_data(self.Block_byte_size)
    return os.urandom(byte_size)

class p_oram:
    def __init__(self, L = 3, Z = 1, C = 8, B=8):
        self.default_bucket = {"valid": 0, "notdummy": 0, "block_num":0, "Data":0}

        #Initialize binary tree
        self.btree = binary_tree.BinaryTree(self.default_bucket)
        self.btree.root = self.btree.create_full_binary_tree(L+1, self.default_bucket)
        self.btree.find_paths_to_leaves()
        self.leaves_list = list(self.btree.leaf_paths.keys())

        #Initialize Pos Map
        self.pos_map = {} #key is block_num and value is node ID of leaf

        #Initialize Stash
        self.stash = []

        self.Block_byte_size = B

    def print_btree(self):
        self.btree.inorder_traversal(self.btree.root)

    def ORAM_read(self, block_num):
        #Client provides block_num for required data block (in RAM)

        #Use Pos Map to determine leaf / path to check
        leaf_id = self.pos_map[block_num]
        leaf_path = self.btree.leaf_paths[leaf_id]

        #Pop entire path from Binary tree and store in stash
        self.stash_populate(leaf_path)

        #Retrieve bucket / block of interest and get RAM address
        for block in self.stash:
            if((block['block_num'] == block_num) and (block["valid"])):
                client_block = block
        
        #Retrieve data from ORAM using actual address
        block_data = block["Data"]
        
        #Return data to client
        return block_data

    def stash_populate(self, path):
        node = self.btree.root
        for i in path:
            if(node.data["vaid"]):
                self.stash.append(node.data)
                node.data = self.default_bucket
            if(i):
                node = node.right
            else:
                node = node.left

    def ORAM_write(self, block_num, data):
        #generate random leaf choice
        leaf_candidate = random.choice(self.leaves_list)
        status = self.add_to_btree(node=self.btree.root, data=data, block_num=block_num, notdummy=1, random_leaf_path=self.btree.leaf_paths[leaf_candidate])
        if(status["data_placed"]):
            print(f"Successfully placed data in path to leaf {leaf_candidate}")
            self.pos_map[block_num] = leaf_candidate
        else:
            print("Failed to place data")


    def add_to_btree(self, node, data, block_num, notdummy, random_leaf_path):
        if(len(random_leaf_path)):
            if(random_leaf_path[0]):
                status = self.add_to_btree(node=node.right, data=data, block_num=block_num, notdummy=notdummy, random_leaf_path=random_leaf_path[1:])
            else:
                status = self.add_to_btree(node=node.left, data=data, block_num=block_num, notdummy=notdummy, random_leaf_path=random_leaf_path[1:])
            
            if(status["data_placed"]):
                    return status
            else:
                if(node.data["valid"]):
                    return {"node":node, "data_placed":0}
                else:
                    node.data = {"valid": 1, "notdummy": notdummy, "block_num":block_num, "Data":data}
                    return {"node":node, "data_placed":1}
        
        #is current node a leaf
        if(node.data["valid"]):
            return {"node":node, "data_placed":0}
        else:
            node.data = {"valid": 1, "notdummy": notdummy, "block_num":block_num, "Data":data}
            return {"node":node, "data_placed":1}


    def periodic_stash_eviction(self):
        return ""





# Example usage
if __name__ == '__main__':
 poram_instance = p_oram()
 poram_instance.print_btree()

 #add a few entries into ORAM
 random_data = generate_random_data(8)
 poram_instance.ORAM_write(69, random_data)

 poram_instance.print_btree()


