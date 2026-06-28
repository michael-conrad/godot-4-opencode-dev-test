#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Ollama HTTP Client

Wrapper for Ollama REST API with error handling and retries.
Ollama is expected to be running as a system service on http://localhost:11434
"""

import requests
import json
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class OllamaConfig:
    """Configuration for Ollama client."""
    host: str = "http://localhost"
    port: int = 11434
    timeout: int = 300
    max_retries: int = 3
    retry_delay: float = 2.0


class OllamaClient:
    """Client for interacting with Ollama API."""

    def __init__(self, config: Optional[OllamaConfig] = None):
        self.config = config or OllamaConfig()
        self.base_url = f"{self.config.host}:{self.config.port}"
        self.session = requests.Session()

    def list_models(self) -> List[str]:
        """List all available models."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/tags",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Chat completion request to Ollama.
        
        Args:
            model: Model name (e.g., 'qwen3.6:35b-256k')
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            stream: Whether to stream response
        
        Returns:
            Response dict with 'message' key containing the response
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream
        }

        for attempt in range(self.config.max_retries):
            try:
                response = self.session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=self.config.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}/{self.config.max_retries}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay)
            except requests.exceptions.ConnectionError:
                logger.error(f"Connection error on attempt {attempt + 1}/{self.config.max_retries}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay)
            except Exception as e:
                logger.error(f"Chat request failed: {e}")
                raise

        raise RuntimeError(f"Failed after {self.config.max_retries} retries")

    def embed(
        self,
        model: str,
        text: str
    ) -> List[float]:
        """
        Generate embeddings using Ollama.
        
        Args:
            model: Embedding model name (e.g., 'qwen3-embedding:40k')
            text: Text to embed
        
        Returns:
            List of floats representing the embedding vector
        """
        payload = {
            "model": model,
            "prompt": text
        }

        for attempt in range(self.config.max_retries):
            try:
                response = self.session.post(
                    f"{self.base_url}/api/embeddings",
                    json=payload,
                    timeout=self.config.timeout
                )
                response.raise_for_status()
                data = response.json()
                return data.get("embedding", [])
            except Exception as e:
                logger.error(f"Embedding request failed (attempt {attempt + 1}): {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay)
                else:
                    raise

    def health_check(self) -> bool:
        """Check if Ollama server is healthy."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
