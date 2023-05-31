cmake_minimum_required(VERSION 3.17)

project(kdtree)

include_directories(include)
add_subdirectory(src)
add_subdirectory(test)

include(CTest)
add_test(NAME TestSetup COMMAND true)
