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
    // This function should be simple.
    fillTree(tree, bucket_size, L);
    return true;

}

bool PathORAM::initializePositionMap() {
    // do DFS: For every path in the DFS order, add an entry to the table
    // The number of paths is given by
    int path[L];
    betterDfs(tree, path, 0, position_map);
    // on successful execution of this method, this will return true.
    return true;
}


bool PathORAM::updatePostitionMap(int position[]) {
    return true;
}

bool PathORAM::accessAddr(Addr addr, char cmd, uint8_t *data) {
    return true;
}

vector<Addr> PathORAM::readAddresses() {
    // this function generates read addresses to make the access oblivious.
    // If each bucket has N blocks and the height of the tree is say H, then
    // there will be H x N number of reads.
    vector<Addr>set_of_reads(bucket_size * L);
    // TODO
    return set_of_reads;
}


vector<Addr> PathORAM::writeAddresses() {
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
    // This method prints the position map
    for (int i = 0 ; i < pow(2, L - 1) ; i++) {
        std::cout << i << " : " << std::endl;
        for (int j = 0 ; j < 1 ; j++) {
            std::cout << position_map[i][j] << " ";
        }
        std::cout << std::endl;
    }
}