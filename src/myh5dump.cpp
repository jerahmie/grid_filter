/*
 *
 */

/*
 * Dump the contents of an hdf5 file.
 */
#include <iostream>
#include <sys/stat.h>
#include <string>
#include "H5Cpp.h"

void usage(){
  std::cout << "usage: myh5dump filename\n" << std::endl;
};

// Operator function
extern "C" herr_t file_info(hid_t loc_id, const char *name,
                            const H5L_info_t *linfo, void *opdata);


int print_header(const std::string & filename) {
  try
  {
  H5::H5File my_h5file;
  std::cout << "Opening file: " << filename << '\n';
  my_h5file = H5::H5File(filename, H5F_ACC_RDONLY);
  std::cout << "Iterate over hdf5 objects.\n";
  herr_t idx = H5Literate(my_h5file.getId(), H5_INDEX_NAME,
                              H5_ITER_INC, NULL, file_info, NULL);

  }
  catch(H5::Exception &e)
  {
    std::cout << "Error in H5 file: " << e.getDetailMsg() << std::endl;
  }
  catch(std::runtime_error &e) 
  {
    std::cout << "Error in execution: " << e.what() << std::endl;
  }
  return 0;
}

int main(int argc, char* argv[]) {

  std::string  filename;
 if (argc == 2) {
    struct stat buffer;
    if (stat(argv[1], &buffer) == 0) {
      std::cout << "found file: " << filename << '\n';
      filename = argv[1];
    } else { 
      std::cout << " File (" << argv[1] << ") not found. \n\n" << "Exiting.\n\n";
      exit(EXIT_FAILURE);
    }
  } else {
    usage();
    exit(EXIT_FAILURE);
  }
 print_header(filename);
}

/*
 * Operator function.
 */
herr_t
file_info(hid_t loc_id, const char *name, const H5L_info_t *linfo, void *opdata)
{
  hid_t group;
    /*
     * Open the group using its name.
     */
    group = H5Gopen2(loc_id, name, H5P_DEFAULT);
    /*
     * Display group name.
     */
    std::cout << "Name : " << name << std::endl;
    H5Gclose(group);
    return 0;
}
