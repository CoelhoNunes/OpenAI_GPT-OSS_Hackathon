import os
import httpx
import asyncio


async def _chat_once() -> str:
    base = os.getenv("VLLM_BASE_URL", "http://localhost:8003")
    # If running inside compose, point to service name
    if "CI" in os.environ:
        base = os.getenv("VLLM_BASE_URL", "http://vllm:8000")
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            f"{base}/v1/chat/completions",
            json={
                "model": os.getenv("MODEL_ID", "openai/gpt-oss-20b"),
                "messages": [{"role": "user", "content": "Say hi"}],
                "max_tokens": 8,
            },
        )
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()


def test_vllm_smoke():
    content = asyncio.get_event_loop().run_until_complete(_chat_once())
    assert isinstance(content, str) and len(content) > 0


