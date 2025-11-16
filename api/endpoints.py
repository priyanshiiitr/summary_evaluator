# api/endpoints.py

import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict

from .schemas import EvaluationRequest, EvaluationResponse
from services.evaluation_service import evaluate_parameter_async
from core.config import get_settings, Settings
from core.scoring import aggregate_scores, synthesize_explanation
from utils.preprocessing import validate_input

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/evaluate", response_model=EvaluationResponse, tags=["Evaluation"])
async def evaluate_summary(request: EvaluationRequest, settings: Settings = Depends(get_settings)):
    """
    Evaluates a summary against a transcript based on specified parameters.
    """
    try:
        # 1. Input Pre-processing and Validation
        validate_input(request.transcript, request.summary)
    except ValueError as e:
        logger.warning(f"Input validation failed: {e}")
        raise HTTPException(status_code=422, detail=str(e))

    metric_results = {}

    # 3. Granular, Parameter-Driven Prompting
    for param in request.evaluation_parameters:
        if param not in settings.evaluation_parameters:
            logger.warning(f"Requested parameter '{param}' not found in configuration.")
            continue
        try:
            logger.info(f"Evaluating parameter: {param}")
            result = await evaluate_parameter_async(
                transcript=request.transcript,
                summary=request.summary,
                parameter_config=settings.evaluation_parameters[param]
            )
            metric_results[param] = result
        except Exception as e:
            logger.error(f"Error evaluating parameter '{param}': {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"An error occurred while evaluating '{param}'.")

    if not metric_results:
        raise HTTPException(status_code=400, detail="No valid evaluation parameters were processed.")

    # 4. Scoring and Explanation Synthesis
    logger.info("Aggregating scores and synthesizing explanation.")
    final_score = aggregate_scores(metric_results, settings.scoring_weights)
    final_explanation = synthesize_explanation(metric_results)

    return EvaluationResponse(
        final_score=final_score,
        explanation=final_explanation,
        metric_details=metric_results
    )
