# tests/test_scoring.py

import pytest
from core.scoring import aggregate_scores, synthesize_explanation
from api.schemas import MetricDetail

@pytest.fixture
def metric_results():
    return {
        "coverage": MetricDetail(score=9.0, explanation="Excellent coverage."),
        "clarity": MetricDetail(score=7.0, explanation="Slightly verbose."),
        "accuracy": MetricDetail(score=8.0, explanation="Factually correct.")
    }

def test_aggregate_scores_with_weights(metric_results):
    weights = {"coverage": 0.5, "clarity": 0.2, "accuracy": 0.3}
    expected_score = (9.0 * 0.5) + (7.0 * 0.2) + (8.0 * 0.3) # 4.5 + 1.4 + 2.4 = 8.3
    assert aggregate_scores(metric_results, weights) == pytest.approx(8.3)

def test_aggregate_scores_partial_weights(metric_results):
    weights = {"coverage": 0.7, "accuracy": 0.3} # clarity is missing
    expected_score = (9.0 * 0.7 + 8.0 * 0.3) / (0.7 + 0.3) # 6.3 + 2.4 = 8.7
    assert aggregate_scores(metric_results, weights) == pytest.approx(8.7)

def test_aggregate_scores_no_weights(metric_results):
    weights = {}
    expected_score = (9.0 + 7.0 + 8.0) / 3 # Simple average
    assert aggregate_scores(metric_results, weights) == pytest.approx(8.0)

def test_synthesize_explanation(metric_results):
    explanation = synthesize_explanation(metric_results)
    assert "Overall assessment:" in explanation
    assert "**Coverage (Score: 9.0):** Excellent coverage." in explanation
    assert "**Clarity (Score: 7.0):** Slightly verbose." in explanation
    assert len(explanation) > 50
