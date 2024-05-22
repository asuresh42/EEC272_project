// There should not be any standard include files
#include "backend.hh"

Stash::Stash(int size) {
    // Initialize the size
    this->size = size;
    // We might use this class to implement some of the stash optimizations
}

PathORAM::PathORAM(int block_size, int L, int bucket_size, bool test) {
    // Let us try to simulate 1 GiB of memory.

    this->block_size = block_size;
    this->L = L;
    this->bucket_size = bucket_size;
    this->test = test;

    // calculate the size of the dram that we are trying to simulate; the
    // getter should now be valid.
    size_of_dram = this->block_size * this->bucket_size * (pow(2, this->L) - 1);

    // We need to initialize the tree
    assert(initializeTree());

    // Now we need to initialize the initial positions
    assert(initializePositionMap());

}

bool PathORAM::initializeTree() {
    // We need to use a binary tree object. For every pathoram object, there
    // can atmost be only one binary tree object. We'll declare it in the 
    // private scope of this class.
    // 
    // first create the root and then automatically fill up the edges. Each
    // block has n number of buckets.
    tree = createNode(bucket_size);
    // This function should be simple. The firxt level is already created!
    fillTree(tree, bucket_size, L - 1);
    return true;

}

bool PathORAM::initializePositionMap() {
    // do DFS: For every path in the DFS order, add an entry to the table
    // The number of paths is given by
    vector<int>path(L);
    betterDfs(tree, path, 0);
    initializePathMap();
    // on successful execution of this method, this will return true.
    return true;
}


vector<int> PathORAM::updatePostitionMap(Addr addr, vector<int>old_position) {
    // This method returns a new position for a given address and its old
    // position
    // int path = get
    vector<int>new_position(L);
    // The new position will stay the same until the common ancestor
    size_t common_ancestor = findLowestCommonAncestor(old_position,
                                                        new_position);
    // for (size_t i = 0 ; i < )
    return new_position;
}

vector<int> PathORAM::getPosition(Addr addr) {
    // This should return the position for a given address
    vector<int>position(L);
    // This should give the block address.
    int block = addr / (bucket_size * block_size);
    int bucket = (addr / block_size) % bucket_size;
    // Search the DFS map for all paths crossing the given block_index
    // FIXME: This is very inefficient!
    for (int i = 0 ; i < pow(2, L - 1) ; i++) {
        vector<int> temp_vec = position_map[i];
        for (int j = 0 ; j < L ; j++)
            if (temp_vec[j] == block) {
                position = temp_vec;
                // We found the first path! Just break it for now.
                break;
            }
    }
    return position;
}

bool PathORAM::accessAddr(Addr addr, char cmd, uint8_t *data) {
    // This is a copy-paste of the python code. There are some filler code to
    // simply test the module. 

    // Now we need to read a path where this block is an element. We can just
    // read the first path where this block is an element of.

    // std::cout << block << " " << bucket << std::endl;

    // Set an address bounds check
    if (addr < 0x0 || addr >= size_of_dram) {
        assert(false && "addr out of bounds!");
    }

    vector<int> position = getPosition(addr);
    for (int i = 0 ; i < L ; i++)
        std::cout << position[i] << " ";

    // generate read requests for this position
    vector<Addr>set_of_reads = readAddresses(position);
    for (int i = 0 ; i < L * bucket_size ; i++)
        std::cout << "0x" << std::hex << set_of_reads[i] << std::dec << std::endl;
    
    Addr incoming_block = addr % bucket_size;

    Addr target_block_index = incoming_block;

    // updatePositionMap(addr, position);
    return true;
}

vector<Addr> PathORAM::readAddresses(vector<int> position) {
    // this function generates read addresses to make the access oblivious.
    // If each bucket has N blocks and the height of the tree is say H, then
    // there will be H x N number of reads.
    vector<Addr>set_of_reads(bucket_size * L);
    int read_index = 0;
    // First get the node.
    for (int i = 0 ; i < L ; i ++) {
        int block_index = position[i];
        // Now get the blocks
        for (int j = 0 ; j < bucket_size ; j++) {
            set_of_reads[read_index++] = block_index * (block_size * bucket_size) + j * block_size; 
        }
    }
    return set_of_reads;
}


vector<Addr> PathORAM::writeAddresses(vector<int> position) {
    // this function generates write addresses to make the access oblivious.
    // If each bucket has N blocks and the height of the tree is say H, then
    // there will be H x N number of reads.
    vector<Addr>set_of_writes(bucket_size * L);
    // TODO
    return set_of_writes;
}

unsigned int PathORAM::getSizeInB() {
    return size_of_dram;
}

unsigned int PathORAM::getSizeInMiB() {
    return size_of_dram/1024/1024;
}

void PathORAM::printPositionMap() {
    // This method prints the position map for debugging.
    for (int i = 0 ; i < pow(2, L - 1) ; i++) {
        std::cout << position_map.size() << " " << i << " : ";
        for (int j = 0 ; j < L ; j++)
            std::cout << position_map[i][j] << " ";
        std::cout << std::endl;
    }
}

size_t PathORAM::findLowestCommonAncestor(std::vector<int>arr1,
                                        std::vector<int>arr2) {
    assert(arr1.size() == arr2.size());
    int index = -1;
    for (size_t i = 0 ; i < arr1.size() ; i++) {
        if (arr1[i] != arr2[i]) {
            index = i;
            break;
        }
    }
    // There has to be a common ancestor!
    assert(index != -1);
    return index;
}

void PathORAM::initializePathMap() {
    // This is the reverse position map
    for (int i = 0 ; i < pow(2, L - 1) ; i++)
        path_map[position_map[i]] = i;
}