#include "src/backend.hh"

int main() {
    // Create an ORAM object. Let us simulate a 1 GiB DRAM device.
    PathORAM PO(64, 4, 4, true);
    std::cout << "Simulating " << PO.getSizeInMiB() << " MiB memory device!" << std::endl;
    // PO.printPositionMap();

    // Try accessing an address
    PO.accessAddr(0xF00 - 64, 'R', nullptr);
    PO.accessAddr(0xF00 - 64, 'R', nullptr);
    return 0;
}