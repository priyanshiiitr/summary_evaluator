# core/scoring.py

from typing import Dict
from api.schemas import MetricDetail

def aggregate_scores(metric_results: Dict[str, MetricDetail], weights: Dict[str, float]) -> float:
    """
    Calculates the final weighted score from individual metric scores.
    """
    total_score = 0.0
    total_weight = 0.0

    for param, result in metric_results.items():
        weight = weights.get(param, 0)
        if weight > 0:
            total_score += result.score * weight
            total_weight += weight

    if total_weight == 0:
        # Fallback to simple average if no weights are applicable
        scores = [r.score for r in metric_results.values()]
        return sum(scores) / len(scores) if scores else 0.0

    return total_score / total_weight

def synthesize_explanation(metric_results: Dict[str, MetricDetail]) -> str:
    """
    Combines individual explanations into a single, coherent paragraph.
    """
    if not metric_results:
        return "No evaluation was performed."

    parts = ["Overall assessment:"]
    for param, result in metric_results.items():
        parts.append(f"**{param.capitalize()} (Score: {result.score:.1f}):** {result.explanation}")
    
    return "\n\n".join(parts)
