"""
utils/llm/prompt_builder.py
"""


def build_note_prompt():

    return """
    Generate realistic test note data.

    Return ONLY valid JSON.

    Example:

    {
        "title": "Meeting Notes",
        "description": "Discussion about sprint planning"
    }

    Do not return explanations.
    """