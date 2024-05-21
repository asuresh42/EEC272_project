cmake_minimum_required(VERSION 3.9.1)
project(PathORAM)


set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -pthread -std=c++11")
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/)

add_executable(oram src/backend.hh src/backend.cc src/binary_tree.hh src/binary_tree.cc main.cc)