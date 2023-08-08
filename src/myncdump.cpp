/*
 * myncdump.cpp
 *
 */

#include <iostream>
#include <sys/stat.h>
#include <string>
#include <netcdf> 


class MPASFile{
  private:
    int ncid = 0;
    int retval = 0;
    void mperr(int); 

  public:
   MPASFile(std::string& );
   ~MPASFile();
   int read_dim(std::string);
   std::vector<float> read_var_1d_float(std::string, int);
};

MPASFile::MPASFile(std::string &filename){
  if (retval = nc_open(filename.c_str(), NC_NOWRITE, &ncid)) {
   mperr(retval); 
  }
}

MPASFile::~MPASFile() {
  if (retval = nc_close(ncid)) { mperr(retval); }
}

void MPASFile::mperr(int e) {
  std::cout << "Error: " << nc_strerror(e) << '\n';
}

// Read dimension from file.
int MPASFile::read_dim(std::string dim_name) {
  int dimid = 0;
  size_t dimval = 0;
  if (retval = nc_inq_dimid(ncid, dim_name.c_str(), &dimid)) { mperr(retval); }
  if (retval = nc_inq_dimlen(ncid, dimid, &dimval)) { mperr(retval); }
  return static_cast<int>(dimval);
}

// Read 1d float variable
std::vector<float> MPASFile::read_var_1d_float(std::string varname, int n) {
  int varid; 
  float data[n]; 
  if (retval = nc_inq_varid(ncid, varname.c_str(), &varid)) { mperr(retval); } 
  if (retval = nc_get_var_float(ncid, varid, &data[0])) { mperr(retval); } 
  std::vector<float> var1d(data, data+n);
  return var1d;
}

void usage() {
  std::cout << "usage: myncdump filename\n" << std::endl;
}

void print_header(std::string &filename) {
  std::cout << "print_header: filename: " << filename << '\n';
  MPASFile mpf = MPASFile(filename);
  int ncells = mpf.read_dim("nCells"); 
  std::cout << "nCells: " << ncells << '\n';
  std::cout << "nEdges: " << mpf.read_dim("nEdges") << '\n';
  std::cout << "nVertices: " << mpf.read_dim("nVertices") << '\n';
  std::vector<float> latcell = mpf.read_var_1d_float("latCell", ncells);
  std::vector<float> loncell = mpf.read_var_1d_float("latCell", ncells);
  for (int i=0; i<ncells; i++) {
    std::cout << '(' << latcell[i] << ", " << loncell[i] << ", " << i+1 << ')' << '\n';
  }
}

int main(int argc, char* argv[])
{
  std::string filename;
  std::cout << "Hello NetCDF \n";
  if (argc == 2) {
    struct stat buffer;
    if (stat(argv[1], &buffer) == 0) {
      filename = argv[1];
      std::cout << "found file: " << filename << '\n'; 
    } else {
      std::cout << "File(" << argv[1] << ") not found. \n\n" << "Exiting.\n\n";
      exit(EXIT_FAILURE);
    }
  } else {
    usage();
    exit(EXIT_FAILURE);
  }
  print_header(filename);
  
}
