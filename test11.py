import random
from DRAM_init import client_DRAM

dram = client_DRAM(block_size=32, number_of_blocks=16)
dram.print_DRAM_contents()