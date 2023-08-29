cmake_minimum_required(VERSION 3.17)

project(kdtree CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

message(STATUS "Appending CMAKE_MODULE_PATH...")
list( APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Modules" )
message(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")

enable_testing()
include_directories(include)
add_subdirectory(src)
add_subdirectory(test)
add_subdirectory(examples)

#[=[
include(CTest)
add_test(NAME TestSetup COMMAND true)
]=]
