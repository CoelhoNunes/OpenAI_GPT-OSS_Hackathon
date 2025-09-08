#pragma once

#include <vector>
#include <string>

// CUDA kernel declarations
extern "C" {
    // Array operations
    void cuda_two_sum_generate(int* nums, int n, int target, int* result, int seed);
    void cuda_rotate_array_generate(int* nums, int n, int k, int* result, int seed);
    void cuda_product_except_self_generate(int* nums, int n, int* result, int seed);
    
    // String operations
    void cuda_group_anagrams_generate(char** strings, int n, int* result, int seed);
    void cuda_longest_substring_generate(char* s, int n, int* result, int seed);
    
    // Expected output computation
    void cuda_compute_expected_output(const char* template_slug, void* input_data, void* output_data, int size);
    
    // Utility functions
    bool cuda_available();
    void cuda_init();
    void cuda_cleanup();
}
