
#include <iostream>
#include <cstdio>
#include <limits>


char format[]  = "%16s %4d %10d %10d %10d %20e %20e \n";

char title_format[]  = "%16s %4s %10s %10s %10s %20s %20s \n";

template <class T>
void print_numeric_info(const char *type)
{

  printf(format
    ,type
    ,sizeof(T)
    ,std::numeric_limits<T>::min()
    ,std::numeric_limits<T>::max()
    ,std::numeric_limits<T>::digits10
    ,std::numeric_limits<T>::min_exponent
    ,std::numeric_limits<T>::max_exponent
  );
  
}

int main() {


  printf(title_format,"type","size", "min", "max", "digits10", "minexp", "maxexp");

  // print the size of int, and max absolute value
  print_numeric_info<int>("int");

  // print the size of unsigned, and max values
  print_numeric_info<unsigned>("unsigned");

  // print the size of long, and max value
  print_numeric_info<long>("long");

  // print the size of short, and max value
  print_numeric_info<short>("short");

  // print the size of float
  print_numeric_info<float>("float");

  // print the size of double
  print_numeric_info<double>("double");

  // print the size of long double
  print_numeric_info<long double>("long double");

  return 0;
}
