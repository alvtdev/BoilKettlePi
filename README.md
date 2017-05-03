# MashberryPi

Automated boil kettle controller on the RaspberryPi

## WiringPi CMake issues

Add the following file, named `FindWiringPi.cmake` to the directory 
`/usr/share/cmake-x.x/Modules`:

```
find_library(WIRINGPI_LIBRARIES NAMES wiringPi)
find_path(WIRINGPI_INCLUDE_DIRS NAMES wiringPi.h)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(wiringPi DEFAULT_MSG WIRINGPI_LIBRARIES WIRINGPI_INCLUDE_DIR)
```
