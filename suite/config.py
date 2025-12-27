"""
Shared configuration for the Authority Separation Evaluation Suite
"""
import os
from dataclasses import dataclass
from typing import Dict, Any, Optional

# Deterministic seed for reproducible results
DEFAULT_SEED = 42

@dataclass
class SuiteConfig:
    # Model configuration
    model_provider: str = "mock"  # "openai", "anthropic", or "mock"
    model_name: str = "gpt-4"
    api_key: Optional[str] = None
    
    # Run configuration
    seed: int = DEFAULT_SEED  # Deterministic seed for reproducibility
    quick_mode: bool = False  # Smaller datasets for testing
    output_dir: str = "artifacts"
    
    # Test-specific configs
    test1_enabled: bool = True
    test2_enabled: bool = True
    test3_enabled: bool = True
    test4_enabled: bool = True
    
    def __post_init__(self):
        # Load from environment
        if self.model_provider != "mock":
            if self.model_provider == "openai":
                self.api_key = os.getenv("OPENAI_API_KEY")
            elif self.model_provider == "anthropic":
                self.api_key = os.getenv("ANTHROPIC_API_KEY")

def get_default_config() -> SuiteConfig:
    return SuiteConfig()

# Test configurations
TEST_CONFIGS = {
    "test1_prompt_injection": {
        "name": "Tool Authority",
        "metric": "unauthorized_tool_use_rate",
        "description": "Rate of unauthorized tool executions"
    },
    "test2_refuse_or_cite": {
        "name": "Epistemic Authority",
        "metric": "hallucination_rate", 
        "description": "Rate of unsupported claims in responses"
    },
    "test3_cost_correctness": {
        "name": "Execution Authority",
        "metric": "tokens_per_task_at_threshold",
        "description": "Tokens per task at >=80% correctness"
    },
    "test4_one_shot_constraints": {
        "name": "Temporal Authority",
        "metric": "catastrophes_after_first",
        "description": "Catastrophic failures after initial learning"
    }
}