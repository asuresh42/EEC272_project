import random
import math

class external_DRAM:

    def __init__(self, block_size, number_of_blocks):
        self.block_size = block_size    # size in bits
        self.number_of_blocks = number_of_blocks

        self.block_addr_arr = [random.randrange(0x00f, 0xfff) for i in range(number_of_blocks)]
        self.bit_max =  2 ** block_size - 1
        self.block_data_arr = [random.randrange(0, self.bit_max) for i in range(number_of_blocks)]
        # memory initialized like array : block_addr <=> block_data
        self.addr_full_arr_dict = {self.block_addr_arr[i] : self.block_data_arr[i] for i in range(number_of_blocks)}      


    def print_DRAM_contents(self):
        # Print key-value pairs using block_addr_arr and block_data_arr in hex and bin
        for k in range(self.number_of_blocks):
            key = self.block_addr_arr[k]
            value = self.block_data_arr[k]
            print(f"Key: {key:08X}, Value: {value:032b}")



class ORAM_controller:

    def __init__(self, number_of_blocks, bucket_size):

        self.number_of_nodes = math.ceil(number_of_blocks/bucket_size)

    
    def init_first_PosMap(self):
        self.PosMap = {}
        for i in range(self.number_of_blocks):

            self.PosMap[] = [1111] #change, this only to test
        










# Example use
#   dram = DRAM(block_size=32, number_of_blocks=16)
#   dram.print_DRAM_contents()
