SET(CMAKE_CXX_FLAGS "-Wall -O3 -std=c++20" CACHE STRING "")
SET(CMAKE_CXX_FLAGS_DEBUG "" CACHE STRING "")
SET(CMAKE_CXX_FLAGS_RELEASE "-DCGAL_NDEBUG" CACHE STRING "")
SET(CMAKE_BUILD_TYPE "Release" CACHE STRING "")
SET(CMAKE_PREFIX_PATH "/usr/local/boost" CACHE STRING "")
