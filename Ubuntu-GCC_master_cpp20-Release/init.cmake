SET(CMAKE_CXX_FLAGS "-DDONT_USE_BOOST_PROGRAM_OPTIONS -Wall -Wextra -frounding-math -std=c++2a" CACHE STRING "")
SET(CMAKE_CXX_FLAGS_DEBUG "" CACHE STRING "")
SET(CMAKE_CXX_FLAGS_RELEASE "-DCGAL_NDEBUG -O3" CACHE STRING "")
SET(CMAKE_BUILD_TYPE "Release" CACHE STRING "")
SET(CMAKE_PREFIX_PATH "/usr/local/boost" CACHE STRING "")
