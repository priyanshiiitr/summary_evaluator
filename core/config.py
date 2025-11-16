# core/config.py

import yaml
from pydantic import BaseModel
from typing import Dict, Optional
from functools import lru_cache

CONFIG_FILE_PATH = "config.yaml"

class LLMSettings(BaseModel):
    api_key: str
    model: str

class EvaluationParameter(BaseModel):
    name: str
    description: str
    prompt_template: str

class Settings(BaseModel):
    llm: LLMSettings
    evaluation_parameters: Dict[str, EvaluationParameter]
    scoring_weights: Dict[str, float]
    preprocessing: Optional[Dict[str, int]] = {}

@lru_cache()
def get_settings() -> Settings:
    """
    Loads configuration from the YAML file and returns a Pydantic Settings object.
    The result is cached to avoid reading the file multiple times.
    """
    with open(CONFIG_FILE_PATH, 'r') as f:
        config_data = yaml.safe_load(f)
    return Settings(**config_data)

# A global settings instance can be used for convenience if preferred,
# but dependency injection with Depends(get_settings) is generally better.
settings = get_settings()
