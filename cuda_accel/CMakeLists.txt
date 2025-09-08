cmake_minimum_required(VERSION 3.18)
project(cuda_accel)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find CUDA
find_package(CUDA REQUIRED)
find_package(PkgConfig REQUIRED)

# Find pybind11
find_package(pybind11 REQUIRED)

# Include directories
include_directories(${CUDA_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

# CUDA sources
set(CUDA_SOURCES src/kernels.cu)

# Create CUDA library
cuda_add_library(cuda_accel_lib ${CUDA_SOURCES})

# Link CUDA libraries to the CUDA library
target_link_libraries(cuda_accel_lib ${CUDA_LIBRARIES})

# Python bindings
pybind11_add_module(cuda_accel src/bindings.cpp)

# Link the CUDA library to the Python module
target_link_libraries(cuda_accel PRIVATE cuda_accel_lib ${CUDA_LIBRARIES})

# Compile flags
set_target_properties(cuda_accel_lib PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON
    CUDA_NVCC_FLAGS "-fPIC"
)

# Set CUDA architecture
set_property(TARGET cuda_accel_lib PROPERTY CUDA_ARCHITECTURES 75 80 86)

# Install targets
install(TARGETS cuda_accel_lib cuda_accel
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
)