"""
utils/ai/llm_helper.py
Central LLM caller used by all agents.
Reads api_key and api_url from config/config.yaml via config/environment.py
No .env needed — config.yaml is the single source of truth.
"""

import requests
from config.environment import config
from utils.logger import get_logger

logger = get_logger(__name__)


def call_llm(prompt: str, model: str = "LongCat-Flash-Chat", max_tokens: int = 2000) -> str:
    """
    Send a prompt to the LLM and return the text response.
    Uses config.llm.api_key and config.llm.api_url from config.yaml.
    All agents call this function.
    """
    api_key = config.llm.api_key
    api_url = config.llm.api_url

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }

    try:
        logger.debug("call_llm: sending prompt (len=%d) to %s", len(prompt), api_url)
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=config.timeouts.api_timeout,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        logger.debug("call_llm: received response (len=%d)", len(text))
        return text

    except requests.exceptions.HTTPError:
        logger.error("call_llm: HTTP error %s — %s", response.status_code, response.text)
        raise
    except Exception as e:
        logger.error("call_llm: failed — %s", str(e))
        raise