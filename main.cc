#include "src/backend.hh"

int main() {
    // Create an ORAM object. Let us simulate a 1 GiB DRAM device.
    PathORAM PO(64, 8, 4, true);
    std::cout << "Simulating " << PO.getSizeInB() << " MiB memory device!" << std::endl;
    // PO.printPositionMap();

    // Try accessing an address
    PO.accessAddr(0xF00 - 64, 'R', nullptr);
    return 0;
}