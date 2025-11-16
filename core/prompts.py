# core/prompts.py

# Note: Prompts are now externalized to config.yaml and managed via core/config.py
# This file is kept for conceptual clarity but is no longer the source of truth.

# Example of how prompts were structured before externalization:
PROMPT_COVERAGE = """
Evaluate the 'coverage' of the summary based on the provided transcript.

Coverage measures how well the summary captures the key points and main ideas of the transcript without omitting critical information. A high score means all essential topics are included.

**Transcript:**
"""
{transcript}
"""

**Summary:**
"""
{summary}
"""

Provide a score from 0.0 to 10.0 for coverage and a brief explanation for your score. Respond ONLY with a JSON object with 'score' and 'explanation' keys.
"""

PROMPT_CLARITY = """
Evaluate the 'clarity' of the summary.

Clarity refers to how easy the summary is to understand. It should be well-structured, use clear language, and be free of jargon unless it was central to the transcript. A high score means the summary is immediately comprehensible.

**Transcript (for context):**
"""
{transcript}
"""

**Summary to evaluate:**
"""
{summary}
"""

Provide a score from 0.0 to 10.0 for clarity and a brief explanation. Respond ONLY with a JSON object with 'score' and 'explanation' keys.
"""
