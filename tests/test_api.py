# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app
from api.schemas import MetricDetail

client = TestClient(app)

@pytest.fixture
def mock_evaluate_parameter():
    mock_response = MetricDetail(score=8.5, explanation="The summary covers the main points well.")
    with patch('api.endpoints.evaluate_parameter_async', return_value=mock_response) as mock_func:
        yield mock_func

def test_evaluate_summary_success(mock_evaluate_parameter):
    """Test successful evaluation of a summary."""
    payload = {
        "transcript": "This is the full long transcript about AI.",
        "summary": "This is a short summary.",
        "evaluation_parameters": ["coverage", "clarity"]
    }
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "final_score" in data
    assert "explanation" in data
    assert "metric_details" in data
    assert "coverage" in data["metric_details"]
    assert data["metric_details"]["coverage"]["score"] == 8.5
    assert mock_evaluate_parameter.call_count == 2

def test_evaluate_summary_invalid_input():
    """Test API response for invalid input (e.g., empty transcript)."""
    payload = {
        "transcript": "",
        "summary": "This is a summary."
    }
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 422
    assert "Transcript cannot be empty" in response.json()["detail"]

@patch('api.endpoints.evaluate_parameter_async')
def test_evaluate_llm_error(mock_evaluate):
    """Test API response when the LLM service raises an exception."""
    mock_evaluate.side_effect = Exception("LLM API is down")
    payload = {
        "transcript": "This is a valid transcript.",
        "summary": "This is a valid summary.",
        "evaluation_parameters": ["coverage"]
    }
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 500
    assert "An error occurred while evaluating 'coverage'" in response.json()["detail"]
