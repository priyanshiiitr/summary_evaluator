# utils/preprocessing.py

import re
from core.config import get_settings

def clean_text(text: str) -> str:
    """
    Performs basic text cleaning, such as normalizing whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def validate_input(transcript: str, summary: str):
    """
    Validates the input transcript and summary against configured constraints.
    Raises ValueError if validation fails.
    """
    settings = get_settings()
    constraints = settings.preprocessing or {}
    max_transcript_len = constraints.get("max_transcript_length", 50000)
    max_summary_len = constraints.get("max_summary_length", 5000)

    if not transcript or not transcript.strip():
        raise ValueError("Transcript cannot be empty.")
    if not summary or not summary.strip():
        raise ValueError("Summary cannot be empty.")

    if len(transcript) > max_transcript_len:
        raise ValueError(f"Transcript length exceeds the maximum of {max_transcript_len} characters.")
    if len(summary) > max_summary_len:
        raise ValueError(f"Summary length exceeds the maximum of {max_summary_len} characters.")

    return clean_text(transcript), clean_text(summary)
