# EEC272_project

This is the kg branch. I'll make my changes on this branch before mergring with
the other branches.

The project uses the following external modules:
1. DRAMsim3: https://github.com/umd-memsys/DRAMsim3
2. CppArgParse: 

## Using the traces

All the traces used to generate results are in the `traces/` directory.
The input traces are collected either using gem5 or Intel Pintool.
The Pintool addresses are converted using a base address 0x80000000.

Here are the instructions to generate an ORAM trace from a given trace.

```sh
git clone git@github.com:asuresh42/EEC272_project.git
cd EEC272_project
git checkout kg/pathoram
mkdir build
cd build
cmake ..
make -j4

# Goto the trace folder
cd ../traces/input
python3 parser_gem5.py

# This generates a DRAMsim3 trace from --MemoryAccess debug flag

# 0: global: Write from functional of size 64 on address 0x10f3bc0 C
# 0: global: 00000000  89 f4 53 48 89 fb 48 83  ec 38 48 8b 6f 48 65 48    tSH {H l8H oHeH
# 0: global: 00000010  8b 04 25 28 00 00 00 48  89 44 24 30 31 c0 0f ba     %(   H D$01@ :
# 0: global: 00000020  e5 08 73 23 ba 0c 00 00  00 48 89 de 48 89 e7 e8   e s#:    H ^H gh
# 0: global: 00000030  63 b6 fd ff 48 85 c0 74  35 44 89 60 08 48 89 e7   c6} H @t5D ` H g
# 0: global: Write from functional of size 64 on address 0x10f3c00 C
# 0: global: 00000000  e8 01 56 fd ff eb 27 40  f6 c5 80 74 09 31 d2 31   h V} k'@vE t 1R1
# 0: global: 00000010  f6 e8 d8 02 fe ff 40 f6  c5 40 75 12 0f ba e5 09   vhX ~ @vE@u  :e 
# 0: global: 00000020  73 c2 48 89 df e8 3d b3  fd ff 84 c0 74 b6 48 8b   sBH _h=3}  @t6H 
# 0: global: 00000030  44 24 30 65 48 33 04 25  28 00 00 00 74 05 e8 d7   D$0eH3 %(   t hW
# 0: global: Write from functional of size 64 on address 0x10f3c40 C


# go back
cd ../../build

./oram \
    --trace ../traces/input/bt.A.trace \
    --output new.trace \
    --limit 100
```

This generates a pathORAM-based trace, which then can be fed into DRAMsim3.
