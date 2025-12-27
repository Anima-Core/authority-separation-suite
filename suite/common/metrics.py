"""
Metric calculation helpers
"""
from typing import List, Dict, Any, Tuple
import statistics

def calculate_rate(successes: int, total: int) -> float:
    """Calculate a rate metric"""
    if total == 0:
        return 0.0
    return successes / total

def calculate_precision_recall(tp: int, fp: int, fn: int) -> Tuple[float, float, float]:
    """Calculate precision, recall, and F1"""
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1

def calculate_cost_at_threshold(results: List[Dict[str, Any]], correctness_threshold: float = 0.8) -> Dict[str, float]:
    """Calculate cost metrics at a correctness threshold"""
    filtered_results = [r for r in results if r.get('correctness', 0) >= correctness_threshold]
    
    if not filtered_results:
        return {
            'mean_tokens': float('inf'),
            'mean_calls': float('inf'),
            'mean_latency': float('inf'),
            'n_samples': 0
        }
    
    tokens = [r.get('tokens', 0) for r in filtered_results]
    calls = [r.get('model_calls', 0) for r in filtered_results]
    latency = [r.get('latency', 0) for r in filtered_results]
    
    return {
        'mean_tokens': statistics.mean(tokens),
        'mean_calls': statistics.mean(calls),
        'mean_latency': statistics.mean(latency),
        'n_samples': len(filtered_results)
    }

def calculate_pareto_dominance(baseline_results: List[Dict], governed_results: List[Dict]) -> Dict[str, Any]:
    """Calculate Pareto dominance metrics"""
    # Extract cost-correctness pairs
    baseline_pairs = [(r.get('tokens', 0), r.get('correctness', 0)) for r in baseline_results]
    governed_pairs = [(r.get('tokens', 0), r.get('correctness', 0)) for r in governed_results]
    
    # Calculate means
    baseline_mean_cost = statistics.mean([p[0] for p in baseline_pairs])
    baseline_mean_correctness = statistics.mean([p[1] for p in baseline_pairs])
    governed_mean_cost = statistics.mean([p[0] for p in governed_pairs])
    governed_mean_correctness = statistics.mean([p[1] for p in governed_pairs])
    
    # Pareto dominance: governed dominates if it has lower cost AND higher/equal correctness
    dominates = governed_mean_cost < baseline_mean_cost and governed_mean_correctness >= baseline_mean_correctness
    
    return {
        'baseline_cost': baseline_mean_cost,
        'baseline_correctness': baseline_mean_correctness,
        'governed_cost': governed_mean_cost,
        'governed_correctness': governed_mean_correctness,
        'cost_reduction': (baseline_mean_cost - governed_mean_cost) / baseline_mean_cost if baseline_mean_cost > 0 else 0,
        'correctness_delta': governed_mean_correctness - baseline_mean_correctness,
        'pareto_dominates': dominates
    }