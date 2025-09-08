# Migration Notes: Cleanup to GPT-OSS via vLLM Only

This release removes legacy providers and dead code to standardize on GPT-OSS models served via vLLM.

## Breaking Removals
- Removed provider selection (`MODEL_PROVIDER`). Only vLLM path remains.
- Removed Ollama support (code, env vars, docs). Use vLLM service instead.
- Removed Hugging Face Inference fallback code paths.
- Deleted root `CMakeLists.txt` and associated dormant DroneSim build artifacts (unused by Docker Compose).

## Required Actions
- Update your `.env`:
  - Set `GPT_OSS_MODEL=openai/gpt-oss-20b` (default used by compose).
  - Remove `MODEL_PROVIDER`, `OLLAMA_BASE_URL`, and `HF_INFERENCE_URL` if present.
  - Optionally set `HF_TOKEN` for gated model downloads.
- Use `docker compose up -d --build` to start services. vLLM healthcheck may take up to 20 minutes on first run (model download and load).

## Notes on vLLM Health
- Healthcheck path: `http://localhost:8003/v1/models` (proxied to vLLM 8000).
- Start period extended and retries increased to accommodate initial weight download and graph capture.
- On WSL, `pin_memory` is disabled automatically by vLLM and may reduce performance; this is expected.

## Smoke Test
After services are healthy:
```bash
curl -s http://localhost:8000/healthz && \
  curl -s http://localhost:8003/v1/models | jq '.data[0].id' && \
  curl -s http://localhost:8003/v1/chat/completions \
    -H 'Content-Type: application/json' \
    -d '{"model":"openai/gpt-oss-20b","messages":[{"role":"user","content":"Say hi"}],"max_tokens":8}' | jq '.choices[0].message.content'
```
Expected: non-empty assistant content.

## TODO
- If VRAM is constrained, consider lowering `--max-model-len` or using a smaller GPT-OSS model. For now we keep defaults to avoid feature drift.
