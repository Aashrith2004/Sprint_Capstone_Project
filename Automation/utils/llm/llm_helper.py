"""
utils/llm/llm_helper.py
"""

import requests
import json

from config.environment import config

from utils.logger import get_logger

from utils.llm.prompt_builder import (
    build_note_prompt
)

logger = get_logger(__name__)


def generate_note_data():
    """
    MCP-inspired LLM test data generation.
    """

    prompt = build_note_prompt()

    payload = {
        "model": "LongCat-Flash-Chat",

        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "temperature": 0.7
    }

    headers = {
        "Authorization": (
            f"Bearer {config.llm.api_key}"
        ),

        "Content-Type": "application/json"
    }

    try:

        logger.info(
            "Sending request to LLM"
        )

        response = requests.post(
            config.llm.api_url,
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        logger.info(
            f"LLM response: {data}"
        )

        # Extract AI content

        content = (
            data["choices"][0]
            ["message"]["content"]
        )

        logger.info(
            f"Generated content: {content}"
        )

        # Convert JSON string to dictionary

        parsed_data = json.loads(content)

        return {
            "title": parsed_data.get(
                "title",
                "AI Generated Note"
            ),

            "description": parsed_data.get(
                "description",
                "Generated using MCP workflow"
            )
        }

    except Exception as e:

        logger.error(
            f"LLM request failed: {e}"
        )

        # Safe fallback response

        return {
            "title": "Fallback AI Note",

            "description": (
                "Fallback AI Description"
            )
        }