from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI

from spiderlens.io import read_json, write_json


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    base_url: str
    model: str
    temperature: float = 0.0


class CachedLLMClient:
    """OpenAI-compatible chat client with prompt-level disk caching."""

    def __init__(self, config: LLMConfig, cache_dir: Path) -> None:
        self.config = config
        self.cache_dir = cache_dir
        self.client = OpenAI(api_key=config.api_key or "missing", base_url=config.base_url)

    def complete(self, prompt: str, refresh: bool = False) -> dict[str, str]:
        cache_key = self.cache_key(prompt)
        cache_path = self.cache_dir / f"{cache_key}.json"
        if cache_path.exists() and not refresh:
            cached = read_json(cache_path)
            return {"text": cached["text"], "cache_key": cache_key, "cached": "true"}

        response = self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.choices[0].message.content or ""
        write_json(cache_path, {"text": text, "model": self.config.model, "prompt_hash": cache_key})
        return {"text": text, "cache_key": cache_key, "cached": "false"}

    def cache_key(self, prompt: str) -> str:
        payload = {
            "base_url": self.config.base_url,
            "model": self.config.model,
            "temperature": self.config.temperature,
            "prompt": prompt,
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
