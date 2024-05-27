#include<fstream>
#include<string>


#include "src/backend.hh"

using namespace std;

int main() {
    // Create an ORAM object. Let us simulate a 1 GiB DRAM device. We fix the
    // necessary parameters for simulation.
    int block_size = 64;    // The amount of data that the cacheline reads in
                            // the system.
    int L = 23;             // Length of the binary tree. This correlates to
                            // the size of the memory that we are trying to
                            // simulate. 22 -> 1 GiB of memory.
    int bucket_size = 4;    // Each of the nodes in the binary tree holds 4
                            // blocks.
    bool debug = false;     // Enable this to generate print statements.

    // Create the PathORAM object to initialize the ORAM module
    PathORAM PO(block_size, L, bucket_size, debug);

    // Inform the user the amount of memory they are trying to simulate.
    std::cout << "Simulating " << PO.getSizeInMiB() <<
                " MiB memory device!" << std::endl;

    // Try accessing an address
    PO.accessAddr(0xF00 - 64, 'R', nullptr);
    PO.accessAddr(0xF00 - 64, 'R', nullptr);

    // TODO: Read a DRAMsim3 trace and generate another trace with oblivious
    // memory accesses. Plagiarism warning: file handling code cpoied from the
    // internet (Geeksforgeeks) to save time.

    // Create a text string, which is used to output the text file
    string trace_line;

    // Read from the trace file
    ifstream TraceInput("../ext/dram.trace");

    // Use a while loop together with the getline() function to read the file
    // line by line
    if (!TraceInput) {
        std::cout << "fatal: trace file not found!" << std::endl;
    }
    else {
        while (getline (TraceInput, trace_line)) {
            // Output the text from the file
            // std::cout << trace_line[11] << std::endl;

            Addr addr = stoi(trace_line.substr(0, 10), 0, 16);
            char cmd;
            if (trace_line[11] == 'R')
                cmd = 'R';
            else
                cmd = 'W';
            uint64_t time = stoi(trace_line.substr(trace_line.find("  "),
                                    trace_line.size()));

            std::cout << addr << " " << cmd << " " << time << std::endl;
            PO.accessAddr(addr, cmd, time, "oram.trace", true, nullptr);
        }
    }
    
    return 0;
}