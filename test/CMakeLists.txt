cmake_minimum_required(VERSION 3.17)

# libgridfilter tests

include(FetchContent)
FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v3.3.2
  )

FetchContent_MakeAvailable(Catch2)

add_executable(unit_tests
  test_kdtree_node2d.cpp
  test_kdtree.cpp)  # add additional cpp files to test

target_link_libraries(unit_tests PRIVATE
  kdtree Catch2::Catch2WithMain)

list(APPEND CMAKE_MODULE_PATH ${catch2_SOURCE_DIR}/extras)
include(Catch)
catch_discover_tests(unit_tests)


# Python unit tests
#[=[
find_package (Python COMPONENTS Interpreter Development)
message("---> ${Python_Interpreter_FOUND}")
message("---> ${Python_EXECUTABLE}")

if (${Python_Interpreter_FOUND})
  include(CTestPythonUnittests.cmake)
endif()

add_test(NAME TestSetup COMMAND true)  # should always pass
]=]
