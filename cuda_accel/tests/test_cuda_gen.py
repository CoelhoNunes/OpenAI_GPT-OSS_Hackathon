"""
Tests for CUDA acceleration
"""

import pytest
import numpy as np
import sys
import os

# Add the build directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'build'))

try:
    import cuda_accel
    CUDA_AVAILABLE = cuda_accel.cuda_available()
except ImportError:
    CUDA_AVAILABLE = False
    cuda_accel = None


class TestCUDAAcceleration:
    """Test CUDA acceleration functionality."""
    
    def test_cuda_availability(self):
        """Test CUDA availability detection."""
        if cuda_accel:
            # This will be True if CUDA is available, False otherwise
            assert isinstance(cuda_accel.cuda_available(), bool)
        else:
            # If cuda_accel module is not available, skip tests
            pytest.skip("CUDA acceleration module not available")
    
    def test_cuda_initialization(self):
        """Test CUDA initialization."""
        if not CUDA_AVAILABLE:
            pytest.skip("CUDA not available")
        
        # Test initialization
        cuda_accel.cuda_init()
        
        # Test cleanup
        cuda_accel.cuda_cleanup()
    
    def test_two_sum_generation(self):
        """Test Two Sum input generation."""
        if not CUDA_AVAILABLE:
            pytest.skip("CUDA not available")
        
        n = 10
        seed = 12345
        
        nums, i, j = cuda_accel.two_sum_generate(n, seed)
        
        assert len(nums) == n
        assert isinstance(i, int)
        assert isinstance(j, int)
        assert 0 <= i < n
        assert 0 <= j < n
        assert i != j
        
        # Verify that nums[i] + nums[j] gives a valid target
        target = nums[i] + nums[j]
        assert isinstance(target, int)
    
    def test_rotate_array_generation(self):
        """Test Rotate Array input generation."""
        if not CUDA_AVAILABLE:
            pytest.skip("CUDA not available")
        
        n = 8
        k = 3
        seed = 54321
        
        nums, result = cuda_accel.rotate_array_generate(n, k, seed)
        
        assert len(nums) == n
        assert len(result) == n
        assert all(isinstance(x, int) for x in nums)
        assert all(isinstance(x, int) for x in result)
    
    def test_product_except_self_generation(self):
        """Test Product Except Self input generation."""
        if not CUDA_AVAILABLE:
            pytest.skip("CUDA not available")
        
        n = 5
        seed = 98765
        
        nums, result = cuda_accel.product_except_self_generate(n, seed)
        
        assert len(nums) == n
        assert len(result) == n
        assert all(isinstance(x, int) for x in nums)
        assert all(isinstance(x, int) for x in result)
        
        # Verify that result[i] is the product of all elements except nums[i]
        for i in range(n):
            expected_product = 1
            for j in range(n):
                if j != i:
                    expected_product *= nums[j]
            assert result[i] == expected_product
    
    def test_longest_substring_generation(self):
        """Test Longest Substring input generation."""
        if not CUDA_AVAILABLE:
            pytest.skip("CUDA not available")
        
        seed = 11111
        
        s, result = cuda_accel.longest_substring_generate(seed)
        
        assert isinstance(s, str)
        assert isinstance(result, int)
        assert result > 0
    
    def test_deterministic_generation(self):
        """Test that same seed produces same results."""
        if not CUDA_AVAILABLE:
            pytest.skip("CUDA not available")
        
        seed = 12345
        n = 10
        
        # Generate twice with same seed
        nums1, i1, j1 = cuda_accel.two_sum_generate(n, seed)
        nums2, i2, j2 = cuda_accel.two_sum_generate(n, seed)
        
        # Results should be identical
        assert nums1 == nums2
        assert i1 == i2
        assert j1 == j2
    
    def test_different_seeds_produce_different_results(self):
        """Test that different seeds produce different results."""
        if not CUDA_AVAILABLE:
            pytest.skip("CUDA not available")
        
        n = 10
        seed1 = 12345
        seed2 = 67890
        
        nums1, i1, j1 = cuda_accel.two_sum_generate(n, seed1)
        nums2, i2, j2 = cuda_accel.two_sum_generate(n, seed2)
        
        # Results should be different (with high probability)
        assert nums1 != nums2 or i1 != i2 or j1 != j2
    
    def test_cpu_fallback_behavior(self):
        """Test CPU fallback when CUDA is not available."""
        # This test verifies that the functions work even without CUDA
        # by testing the CPU fallback implementations
        
        # We can't easily test this without mocking, but we can verify
        # that the functions don't crash when called
        if cuda_accel:
            try:
                # These should work even without CUDA (CPU fallback)
                cuda_accel.cuda_init()
                nums, i, j = cuda_accel.two_sum_generate(5, 12345)
                assert len(nums) == 5
                cuda_accel.cuda_cleanup()
            except Exception as e:
                # If there's an error, it should be a clear error message
                assert "CUDA" in str(e) or "GPU" in str(e)
    
    def test_memory_management(self):
        """Test that CUDA memory is properly managed."""
        if not CUDA_AVAILABLE:
            pytest.skip("CUDA not available")
        
        # Test multiple generations to ensure no memory leaks
        for _ in range(10):
            nums, i, j = cuda_accel.two_sum_generate(100, 12345)
            assert len(nums) == 100
        
        # Memory should still be accessible after multiple calls
        nums, i, j = cuda_accel.two_sum_generate(50, 54321)
        assert len(nums) == 50
