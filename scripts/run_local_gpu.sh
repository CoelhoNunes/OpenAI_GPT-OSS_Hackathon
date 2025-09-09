#!/usr/bin/env bash
set -euo pipefail

echo "This project runs exclusively on gpt-oss with CUDA, fully local inference."

# Check CUDA availability
if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "[ERROR] NVIDIA drivers/CUDA not detected. Please install drivers and CUDA toolkit." >&2
  exit 1
fi

echo "CUDA detected:"
nvidia-smi || true

# Env
cp -n env.example .env 2>/dev/null || true

# Start stack
docker compose up --build

