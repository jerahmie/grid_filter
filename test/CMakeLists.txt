cmake_minimum_required(VERSION 3.17)

enable_testing()

find_package (Python COMPONENTS Interpreter Development)
message("---> ${Python_Interpreter_FOUND}")
message("---> ${Python_EXECUTABLE}")

if (${Python_Interpreter_FOUND})
  include(CTestPythonUnittests.cmake)
endif()

add_test(NAME TestSetup COMMAND true)  # should always pass

