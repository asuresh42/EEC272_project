#include "src/backend.hh"

int main() {
    // Create an ORAM object. Let us simulate a 1 GiB DRAM device.
    PathORAM PO(64, 3, 4, true);
    std::cout << "Simulating " << PO.getSizeInMiB() << " MiB memory device!" << std::endl;
    PO.printPositionMap();
    return 0;
}