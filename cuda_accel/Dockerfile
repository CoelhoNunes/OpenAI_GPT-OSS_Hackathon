FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    cmake \
    curl \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install pybind11 system-wide for cmake
RUN pip3 install pybind11[global]

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Build CUDA extensions
RUN mkdir -p build && cd build && \
    cmake .. && \
    make -j$(nproc)

# Create non-root user
RUN useradd -m -u 1000 cuda_user && chown -R cuda_user:cuda_user /app
USER cuda_user

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Run the application
CMD ["python3", "server.py"]
