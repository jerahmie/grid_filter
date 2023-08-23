cmake_minimum_required(VERSION 3.17)

project(kdtree CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

enable_testing()
include_directories(include)
add_subdirectory(src)
add_subdirectory(test)
add_subdirectory(examples)

#[=[
include(CTest)
add_test(NAME TestSetup COMMAND true)
]=]
