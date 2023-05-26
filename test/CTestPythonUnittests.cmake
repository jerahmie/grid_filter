# CTest execute python unittests

message("Executing python tests.")
set(pytest_list test_mytest.py test_mpasgrid.py test_maponly.py
    test_kdtree.py test_graph_data.py test_grid_perimeter.py 
    test_kdtree_regional.py)

foreach(pt IN LISTS pytest_list)
  set(pytest_file ${CMAKE_CURRENT_SOURCE_DIR}/python_tests/${pt})
  if (EXISTS ${pytest_file})
    message("Adding python test file: ${pytest_file}")
    add_test(NAME ${pt}
      COMMAND ${Python_EXECUTABLE} ${pytest_file}
      WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/test/python_tests)
  else()
    message("${pytest_file} not found.")
  endif()
endforeach()

#[=[
add_test(NAME python-tests
  COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/python_tests/test_mytest.py
  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/test/python_tests)
#]=]
