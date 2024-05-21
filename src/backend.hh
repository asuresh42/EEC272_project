#ifndef BACKEND_HH
#define BACKEND_HH

#include <iostream>
#include <vector>
#include <map>
#include <cmath>

#include "binary_tree.hh"

// Define Addr as addresses. In this example, we can take in 64 bit addresses.
typedef uint64_t Addr;

using namespace std;

class Stash {
    private:
        Addr addr;
        // The size of the Stash
        int size;
        // We might implement this with a table
        pair<int, Addr>stash_table;
        // The position defines the position of in the stash
        uint32_t position;
    public:
        // The implementation of the stash is TBD
        Stash(int size);
};

class PathORAM {
    /* This class creates an ORAM structure without recursion
        :params:
        block_size : Block size of the ORAM
        bucket size : Size of the leaf bucket
    */
    private:
        // We keep the basic variables as private
        uint64_t size_of_dram;
        int block_size;
        int bucket_size;
        int L;
        bool test;
        // Keep a table for the position. We'll be using this for the remapping
        map<int, int*>position_map;

        struct BTNode *tree;
        // 
    public:
        // The class constructor to initialize the path ORAM module. The block
        // is a processor cache line. So block size is fixed to 64.
        PathORAM(int block_size = 64, int L = 22, int bucket_size = 4, bool test = true);
        // Get the size of the DRAM device. In DRAMsim3, this should be the
        // same as the simulated memory.
        int getSizeOfDRAM();
        // Initialize the PathORAM module. For testing, use initializeTreeTest
        bool initializeTree();
        // Initialize the position map.
        bool initializePositionMap();
        bool updatePostitionMap(int position[]);

        bool accessAddr(Addr addr, char cmd, uint8_t *data = nullptr);
        // If accessAddr returns true, then we have to generate all read
        // addresses.
        vector<Addr>readAddresses();
        // We then need to generate the same number of writes to make the ORAM
        // oblivious.
        vector<Addr>writeAddresses();
        // Looks like ORAM serializes every single memory request.

        // utility functions to debug
        unsigned int getSizeInB();
        unsigned int getSizeInMiB();

        void printPositionMap();
};

#endif