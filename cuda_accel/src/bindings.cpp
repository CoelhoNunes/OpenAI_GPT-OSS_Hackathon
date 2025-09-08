#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>
#include <memory>

// Forward declarations for CUDA functions
extern "C" {
    void* cuda_generate_inputs(int* sizes, int count, int seed);
    void* cuda_compute_expected(int* inputs, int input_size, int* expected, int expected_size);
    void cuda_free(void* ptr);
}

namespace py = pybind11;

// Wrapper functions for Python
py::array_t<int> generate_inputs_wrapper(py::array_t<int> sizes, int seed) {
    py::buffer_info sizes_buf = sizes.request();
    int* sizes_ptr = static_cast<int*>(sizes_buf.ptr);
    int count = sizes_buf.size;
    
    void* result = cuda_generate_inputs(sizes_ptr, count, seed);
    if (!result) {
        throw std::runtime_error("CUDA input generation failed");
    }
    
    // Convert result to numpy array (simplified - actual implementation would depend on CUDA kernel output)
    std::vector<int> data(count * 10); // Placeholder size
    return py::cast(data);
}

py::array_t<int> compute_expected_wrapper(py::array_t<int> inputs, py::array_t<int> expected) {
    py::buffer_info inputs_buf = inputs.request();
    py::buffer_info expected_buf = expected.request();
    
    int* inputs_ptr = static_cast<int*>(inputs_buf.ptr);
    int* expected_ptr = static_cast<int*>(expected_buf.ptr);
    
    void* result = cuda_compute_expected(inputs_ptr, inputs_buf.size, expected_ptr, expected_buf.size);
    if (!result) {
        throw std::runtime_error("CUDA expected computation failed");
    }
    
    // Convert result to numpy array
    std::vector<int> data(expected_buf.size);
    return py::cast(data);
}

PYBIND11_MODULE(cuda_accel, m) {
    m.doc() = "CUDA acceleration module for problem generation";
    
    m.def("generate_inputs", &generate_inputs_wrapper, 
          "Generate test inputs using CUDA acceleration",
          py::arg("sizes"), py::arg("seed"));
    
    m.def("compute_expected", &compute_expected_wrapper,
          "Compute expected outputs using CUDA acceleration", 
          py::arg("inputs"), py::arg("expected"));
}