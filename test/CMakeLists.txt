cmake_minimum_required(VERSION 3.17)

# libgridfilter tests

include(FetchContent)
FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v3.3.2
  )

FetchContent_MakeAvailable(Catch2)

find_package(HDF5 REQUIRED COMPONENTS CXX HL)

add_executable(unittests
  test_kdtree_node2d.cpp
  test_kdtree.cpp
  test_kdtree_util.cpp
  test_mpas_file.cpp
  test_mpas_util.cpp
  test_kdtree_regional.cpp
  test_obs_data.cpp)  # add additional cpp files to test

include_directories(${HDF5_INCLUDE_DIRS})

target_link_libraries(unittests PRIVATE
  kdtree
  Catch2::Catch2WithMain
  netcdf
  ${HDF5_CXX_LIBRARIES}
  )

target_compile_options(unittests PRIVATE
	$<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:GNU>>:-Wall>)

list(APPEND CMAKE_MODULE_PATH ${catch2_SOURCE_DIR}/extras)
include(Catch)
catch_discover_tests(unittests)


# Python unit tests
##[=[
find_package (Python COMPONENTS Interpreter Development)
message("---> ${Python_Interpreter_FOUND}")
message("---> ${Python_EXECUTABLE}")

if (${Python_Interpreter_FOUND})
  include(CTestPythonUnittests.cmake)
endif()

add_test(NAME TestSetup COMMAND true)  # should always pass
#]=]
