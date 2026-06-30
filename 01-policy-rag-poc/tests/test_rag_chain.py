import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import config
import rag_chain


class GroqGenerationTests(unittest.TestCase):
    def test_generate_answer_uses_groq_when_api_key_is_present(self):
        chunks = [
            rag_chain.RetrievedChunk(
                text="Example policy text",
                source_file="policy.md",
                section="section",
                score=1.0,
            )
        ]

        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}, clear=False):
            with patch("rag_chain.urllib.request.urlopen") as mock_urlopen:
                class DummyResponse:
                    def read(self):
                        return b'{"choices": [{"message": {"content": "groq answer"}}]}'

                    def __enter__(self):
                        return self

                    def __exit__(self, exc_type, exc, tb):
                        return False

                mock_urlopen.return_value = DummyResponse()
                answer = rag_chain.generate_answer("ask groq What is the policy?", chunks)

        self.assertEqual(answer, "groq answer")

    def test_generate_answer_uses_ollama_when_requested(self):
        chunks = [
            rag_chain.RetrievedChunk(
                text="Example policy text",
                source_file="policy.md",
                section="section",
                score=1.0,
            )
        ]

        with patch.dict(os.environ, {}, clear=True):
            with patch("rag_chain.urllib.request.urlopen") as mock_urlopen:
                class DummyResponse:
                    def read(self):
                        return b'{"response": "ollama answer"}'

                    def __enter__(self):
                        return self

                    def __exit__(self, exc_type, exc, tb):
                        return False

                mock_urlopen.return_value = DummyResponse()
                answer = rag_chain.generate_answer("ask ollama What is the policy?", chunks)

        self.assertEqual(answer, "ollama answer")

    def test_generate_with_groq_uses_configured_endpoint_and_model_settings(self):
        with patch.dict(os.environ, {
            "GROQ_API_KEY": "test-key",
            "GROQ_API_BASE": "https://api.groq.com/openai/v1/chat/completions",
            "GROQ_MODEL": "llama-3.3-70b-versatile",
            "GROQ_MAX_TOKENS": "256",
        }, clear=False):
            with patch("rag_chain.urllib.request.urlopen") as mock_urlopen:
                class DummyResponse:
                    def read(self):
                        return b'{"choices": [{"message": {"content": "groq answer"}}]}'

                    def __enter__(self):
                        return self

                    def __exit__(self, exc_type, exc, tb):
                        return False

                mock_urlopen.return_value = DummyResponse()
                rag_chain.generate_with_groq("Hello", "llama-3.3-70b-versatile")

                request = mock_urlopen.call_args.args[0]
                payload = json.loads(request.data.decode("utf-8"))
                self.assertEqual(request.full_url, "https://api.groq.com/openai/v1/chat/completions")
                self.assertEqual(request.headers["Authorization"], "Bearer test-key")
                self.assertEqual(request.headers["User-agent"], "policy-rag/1.0")
                self.assertEqual(payload["model"], "llama-3.3-70b-versatile")
                self.assertEqual(payload["max_tokens"], 256)

    def test_parse_provider_handles_quoted_prefix(self):
        provider, remainder = rag_chain.parse_provider('"ask ollama what health and wellness benefits are available?"')
        self.assertEqual(provider, "ollama")
        self.assertEqual(remainder, "what health and wellness benefits are available?")

    def test_default_provider_is_ollama(self):
        self.assertEqual(rag_chain.get_default_provider(), "ollama")

    def test_config_loader_reads_values_from_ini_file(self):
        config_path = ROOT / "config" / "config.ini"
        with patch.object(config, "CONFIG_PATH", config_path):
            value = config.get_setting("groq_model", section="api")
            self.assertEqual(value, "llama-3.3-70b-versatile")


if __name__ == "__main__":
    unittest.main()
