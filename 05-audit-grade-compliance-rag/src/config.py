import configparser
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.ini"
LOCAL_CONFIG_PATH = PROJECT_ROOT / "config" / "config.local.ini"


def _load_config_parser():
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH)
    if LOCAL_CONFIG_PATH.exists():
        parser.read(LOCAL_CONFIG_PATH)
    return parser


def get_setting(key: str, default: str = "", section: str = "api") -> str:
    parser = _load_config_parser()
    if parser.has_option(section, key):
        value = parser.get(section, key, fallback="")
        if value:
            return value
    return os.environ.get(key.upper(), default)


def get_api_settings() -> dict:
    parser = _load_config_parser()
    return {
        "groq_api_key": get_setting("groq_api_key"),
        "groq_model": get_setting("groq_model", "llama-3.3-70b-versatile"),
        "groq_api_base": get_setting("groq_api_base", "https://api.groq.com/openai/v1/chat/completions"),
        "groq_max_tokens": get_setting("groq_max_tokens", "1024"),
        "default_provider": get_setting("default", "ollama", section="provider"),
        "ollama_timeout": get_setting("ollama_timeout", "180"),
    }
