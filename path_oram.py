import binary_tree

class p_oram:
    def __init__(self, L = 3, Z = 1, C = 8):
        default_bucket = [{"valid": 0, "dummy": 0, "block_num":0, "RAM_address":0}]

        #Initialize binary tree
        self.btree = binary_tree.BinaryTree(default_bucket)
        self.btree.root = self.btree.create_full_binary_tree(L+1, default_bucket)

        #Initialize Pos Map


        #Initialize Stash

    def __print_btree__(self):
        self.btree.inorder_traversal(self.btree.root)

    def ORAM_access(block_num):
        #Use Pos Map to determine leaf / path
        #Pop entire path from Binary tree and store in stash
        #Retrieve bucket / block of interest and get RAM address
        #Retrieve data from ORAM using actual address
        #Return data to client

    def periodic_stash_eviction():
        pass





# Example usage
if __name__ == '__main__':
 poram_instance = p_oram()
 poram_instance.__print_btree__()


