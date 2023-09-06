cmake_minimum_required(VERSION 3.17)

project(kdtree C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

message(STATUS "Appending CMAKE_MODULE_PATH...")
list( APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Modules" )
message(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")

include_directories(include)
add_subdirectory(src)
add_subdirectory(examples)

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
enable_testing()
add_subdirectory(test)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Intel")
  message(STATUS "SKIPPING Catch2 Unittests for Intel compiler.")
else()
  message(STATUS "SKIPPING Catch2 Unittests for Non-GNU compilers.")
endif()


#[=[
include(CTest)
add_test(NAME TestSetup COMMAND true)
]=]
