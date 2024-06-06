#include<fstream>
#include<string>


#include "src/backend.hh"
#include "ext/cpp-arg-parse/src/argparse.hh"

using namespace std;

int main(int argc, char *argv[]) {


    // using Argparse (beta). use --help to show each of the arguments.
    std::string info = "This program creates an ORAM trace.";

    // we now define all the expected arguments.

    int expected_count = 6;

    // initialize the argparser all the input parameters.
    Argparse args(argc, expected_count, info);
    
    // allocate the required amount of memory fore initializing each of these
    // elements.
    args.allocArgs(expected_count);

    // all the args have their own help statements. this is required to display
    // --help
    args.initArgs(
            "-b", "--block-size", "block-size of the tree", "64"
    );
    args.initArgs(
            "-z", "--bucket-size", "bucket-size of a node", "4"
    );
    args.initArgs(
            "-l", "--length", "length of the tree", "23"
    );
    args.initArgs(
            "-t", "--trace", "supply a trace for the program", ""
    );
    args.initArgs(
            "-o", "--output", "supply an output file name", ""
    );    args.initArgs(
            "-h", "--help", "display this message", ""
    );

    // now, parse each of the supplied arguments, and place them into the
    // correct fields in the setArgs function.
    args.setArgs(argv);

    // check if there is --help or --verbose present in the initial string.
    if(args.getArgs("-h") == "1") {
        // help requested.
        args.printHelpArgs();
        return -1;
    }

    // Create an ORAM object. Let us simulate a 1 GiB DRAM device. We fix the
    // necessary parameters for simulation.

    // The amount of data that the cacheline reads in the system.
    int block_size, bucket_size, L;
    std::cout << args.getArgs("--block-size") << " " << "1" << std::endl;
    if (args.getArgs("--block-size") == "")
        block_size = 64;
    else
        block_size = std::stoi(args.getArgs("--block-size"));
    // Length of the binary tree. This correlates to the size of the memory
    // that we are trying to simulate. 22 -> 1 GiB of memory.
    if (args.getArgs("--length") == "")
        L = 23;
    else
        L = std::stoi(args.getArgs("--length"));
    // Each of the nodes in the binary tree holds 4 blocks.
    if (args.getArgs("--bucket-size") == "")
        bucket_size = 4;
    else
        bucket_size = std::stoi(args.getArgs("--bucket-size"));    
    // Enable this to generate print statements.
    bool debug = false;     
    if(args.getArgs("--verbose") == "1")
        debug = true;

    std::string input_trace, output_trace;
    // get the trace file
    if (args.getArgs("--trace") == "") {
        // The user did not provide any input files!
        std::cout << "Error! No input files provided!" << std::endl;
        args.printHelpArgs();
        return -1;
    }
    else
        input_trace = args.getArgs("--trace");
    // get the trace file
    if (args.getArgs("--output") == "") {
        // The user did not provide any input files!
        std::cout << "Error! No output file path provided!" << std::endl;
        args.printHelpArgs();
        return -1;
    }
    else
        output_trace = args.getArgs("--output");

    if (debug)
        std::cout << "Creating an ORAM module!" << std::endl;

    // Create the PathORAM object to initialize the ORAM module
    PathORAM PO(block_size, L, bucket_size, debug);

    // Inform the user the amount of memory they are trying to simulate.
    std::cout << "Simulating " << PO.getSizeInMiB() <<
                " MiB memory device!" << std::endl;

    // Try accessing an address
    // PO.accessAddr(0xF00 - 64, 'R', nullptr);

    // TODO: Read a DRAMsim3 trace and generate another trace with oblivious
    // memory accesses. Plagiarism warning: file handling code cpoied from the
    // internet (Geeksforgeeks) to save time.

    // Create a text string, which is used to output the text file
    string trace_line;

    // Read from the trace file
    ifstream TraceInput(input_trace);

    // Use a while loop together with the getline() function to read the file
    // line by line
    if (!TraceInput) {
        std::cout << "fatal: trace file not found!" << std::endl;
        return -1;
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
            PO.accessAddr(addr, cmd, time, output_trace, true, nullptr);
        }
    }
    
    return 0;
}