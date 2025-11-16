# services/evaluation_service.py

import logging
import json
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from core.config import get_settings
from core.config import EvaluationParameter
from api.schemas import MetricDetail

logger = logging.getLogger(__name__)

# Initialize the OpenAI client once
settings = get_settings()
client = AsyncOpenAI(api_key=settings.llm.api_key)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
async def evaluate_parameter_async(transcript: str, summary: str, parameter_config: EvaluationParameter) -> MetricDetail:
    """
    Asynchronously evaluates a single parameter by sending a formatted prompt to the LLM.
    """
    prompt = parameter_config.prompt_template.format(
        transcript=transcript,
        summary=summary
    )

    try:
        logger.info(f"Sending request to LLM for parameter: {parameter_config.name}")
        response = await client.chat.completions.create(
            model=settings.llm.model,
            messages=[
                {"role": "system", "content": "You are an expert evaluator. Your response must be a single JSON object with two keys: 'score' (a float from 0.0 to 10.0) and 'explanation' (a string)."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("LLM returned an empty response.")
        
        logger.debug(f"LLM raw response for {parameter_config.name}: {content}")
        
        parsed_content = json.loads(content)
        
        # Validate parsed content
        if 'score' not in parsed_content or 'explanation' not in parsed_content:
            raise KeyError("LLM response is missing 'score' or 'explanation' key.")
        
        return MetricDetail(**parsed_content)

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from LLM response: {content}", exc_info=True)
        raise ValueError(f"Could not decode LLM JSON response: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during LLM API call for {parameter_config.name}: {e}", exc_info=True)
        raise
