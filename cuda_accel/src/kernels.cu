#include <cuda_runtime.h>
#include <curand.h>
#include <curand_kernel.h>
#include <stdio.h>
#include <stdlib.h>

// CUDA kernel for generating random inputs
__global__ void generate_random_inputs_kernel(int* output, int size, int seed) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        curandState state;
        curand_init(seed + idx, 0, 0, &state);
        output[idx] = curand(&state) % 1000; // Generate random numbers 0-999
    }
}

// CUDA kernel for computing expected outputs (placeholder)
__global__ void compute_expected_kernel(int* inputs, int* outputs, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        // Placeholder computation - actual implementation would depend on problem type
        outputs[idx] = inputs[idx] * 2;
    }
}

// Host function to generate inputs
extern "C" void* cuda_generate_inputs(int* sizes, int count, int seed) {
    int total_size = 0;
    for (int i = 0; i < count; i++) {
        total_size += sizes[i];
    }
    
    int* d_output;
    cudaMalloc(&d_output, total_size * sizeof(int));
    
    int threads_per_block = 256;
    int blocks = (total_size + threads_per_block - 1) / threads_per_block;
    
    generate_random_inputs_kernel<<<blocks, threads_per_block>>>(d_output, total_size, seed);
    cudaDeviceSynchronize();
    
    return d_output;
}

// Host function to compute expected outputs
extern "C" void* cuda_compute_expected(int* inputs, int input_size, int* expected, int expected_size) {
    int* d_inputs, *d_outputs;
    
    cudaMalloc(&d_inputs, input_size * sizeof(int));
    cudaMalloc(&d_outputs, expected_size * sizeof(int));
    
    cudaMemcpy(d_inputs, inputs, input_size * sizeof(int), cudaMemcpyHostToDevice);
    
    int threads_per_block = 256;
    int blocks = (expected_size + threads_per_block - 1) / threads_per_block;
    
    compute_expected_kernel<<<blocks, threads_per_block>>>(d_inputs, d_outputs, expected_size);
    cudaDeviceSynchronize();
    
    cudaMemcpy(expected, d_outputs, expected_size * sizeof(int), cudaMemcpyDeviceToHost);
    
    cudaFree(d_inputs);
    cudaFree(d_outputs);
    
    return expected;
}

// Host function to free CUDA memory
extern "C" void cuda_free(void* ptr) {
    if (ptr) {
        cudaFree(ptr);
    }
}