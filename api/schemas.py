# api/schemas.py

from pydantic import BaseModel, Field
from typing import List, Dict

class EvaluationRequest(BaseModel):
    transcript: str = Field(..., min_length=1, description="The full source text or transcript.")
    summary: str = Field(..., min_length=1, description="The summary text to be evaluated.")
    evaluation_parameters: List[str] = Field(
        default=["coverage", "clarity", "conciseness", "accuracy"],
        description="A list of parameters to evaluate the summary against."
    )

class MetricDetail(BaseModel):
    score: float = Field(..., ge=0, le=10, description="The score for the individual metric.")
    explanation: str = Field(..., description="The LLM's explanation for the score.")

class EvaluationResponse(BaseModel):
    final_score: float = Field(..., ge=0, le=10, description="The final weighted score for the summary.")
    explanation: str = Field(..., description="A synthesized explanation of the overall score.")
    metric_details: Dict[str, MetricDetail] = Field(..., description="A breakdown of scores and explanations for each evaluated metric.")
