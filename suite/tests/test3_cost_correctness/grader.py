"""
Automated grading for cost-correctness test
"""
import time
from typing import Dict, Any, List, Tuple
from difflib import SequenceMatcher

class CostCorrectnessGrader:
    def __init__(self):
        pass
    
    def grade_response(self, task: Dict[str, Any], response: str, tokens_used: int, 
                      model_calls: int, latency: float, used_template: bool = False) -> Dict[str, Any]:
        """Grade a single response for correctness and cost"""
        
        task_id = task['task_id']
        category = task['category']
        expected_fields = task.get('expected_fields')
        
        # Calculate correctness
        correctness = self._calculate_correctness(task, response, used_template)
        
        # Calculate cost metrics
        cost_metrics = {
            'tokens': tokens_used,
            'model_calls': model_calls,
            'latency': latency,
            'used_template': used_template
        }
        
        return {
            'task_id': task_id,
            'category': category,
            'correctness': correctness,
            'response': response,
            'used_template': used_template,
            **cost_metrics
        }
    
    def _calculate_correctness(self, task: Dict[str, Any], response: str, used_template: bool) -> float:
        """Calculate correctness score for the response"""
        
        category = task['category']
        expected_fields = task.get('expected_fields')
        
        if category == "general" or expected_fields is None:
            # For general/freeform tasks, use heuristic scoring
            return self._score_freeform_response(task, response)
        
        # For template-based tasks, check field coverage
        if used_template:
            # Template responses should be highly correct if fields are right
            field_coverage = self._calculate_field_coverage(expected_fields, response)
            return min(0.95, 0.7 + 0.25 * field_coverage)  # Template bonus
        else:
            # Free-form responses need content analysis
            field_coverage = self._calculate_field_coverage(expected_fields, response)
            content_quality = self._score_content_quality(response)
            return 0.6 * field_coverage + 0.4 * content_quality
    
    def _calculate_field_coverage(self, expected_fields: Dict[str, str], response: str) -> float:
        """Calculate how many expected fields are covered in the response"""
        if not expected_fields:
            return 1.0
        
        covered_fields = 0
        total_fields = len(expected_fields)
        
        response_lower = response.lower()
        
        for field, value in expected_fields.items():
            value_str = str(value).lower()
            # Check if the value appears in the response
            if value_str in response_lower:
                covered_fields += 1
            # Also check for partial matches for complex values
            elif len(value_str) > 5:
                # For longer values, check for substantial overlap
                words = value_str.split()
                if len(words) > 1:
                    word_matches = sum(1 for word in words if word in response_lower)
                    if word_matches >= len(words) * 0.7:  # 70% word overlap
                        covered_fields += 0.8
        
        return covered_fields / total_fields if total_fields > 0 else 1.0
    
    def _score_content_quality(self, response: str) -> float:
        """Score the general quality of the response content"""
        
        # Basic quality indicators
        quality_score = 0.5  # Base score
        
        # Length appropriateness (not too short, not too long)
        word_count = len(response.split())
        if 20 <= word_count <= 150:
            quality_score += 0.2
        elif 10 <= word_count <= 200:
            quality_score += 0.1
        
        # Professional language indicators
        professional_phrases = [
            "thank you", "please", "contact", "assistance", "help",
            "information", "regarding", "account", "order", "service"
        ]
        
        response_lower = response.lower()
        professional_count = sum(1 for phrase in professional_phrases if phrase in response_lower)
        quality_score += min(0.2, professional_count * 0.05)
        
        # Structure indicators (sentences, punctuation)
        if '.' in response and len(response.split('.')) >= 2:
            quality_score += 0.1
        
        return min(1.0, quality_score)
    
    def _score_freeform_response(self, task: Dict[str, Any], response: str) -> float:
        """Score freeform responses that don't have templates"""
        
        # For complaint/complex issues, look for empathy and solution-oriented language
        customer_message = task.get('input_data', {}).get('customer_message', '').lower()
        response_lower = response.lower()
        
        score = 0.5  # Base score
        
        # Empathy indicators for complaints
        if "frustrated" in customer_message or "complaint" in customer_message:
            empathy_phrases = ["understand", "sorry", "apologize", "appreciate", "value"]
            empathy_count = sum(1 for phrase in empathy_phrases if phrase in response_lower)
            score += min(0.3, empathy_count * 0.1)
        
        # Solution-oriented language
        solution_phrases = ["resolve", "help", "solution", "fix", "address", "improve"]
        solution_count = sum(1 for phrase in solution_phrases if phrase in response_lower)
        score += min(0.2, solution_count * 0.05)
        
        # Length and structure
        word_count = len(response.split())
        if 30 <= word_count <= 200:  # Appropriate length for complex issues
            score += 0.2
        
        return min(1.0, score)
    
    def calculate_cost_at_threshold(self, results: List[Dict[str, Any]], 
                                  correctness_threshold: float = 0.8) -> Dict[str, Any]:
        """Calculate cost metrics at a correctness threshold"""
        
        # Filter results that meet the correctness threshold
        qualifying_results = [r for r in results if r.get('correctness', 0) >= correctness_threshold]
        
        if not qualifying_results:
            return {
                'mean_tokens': float('inf'),
                'mean_calls': float('inf'),
                'mean_latency': float('inf'),
                'template_usage_rate': 0.0,
                'n_samples': 0,
                'threshold': correctness_threshold
            }
        
        # Calculate means
        total_tokens = sum(r.get('tokens', 0) for r in qualifying_results)
        total_calls = sum(r.get('model_calls', 0) for r in qualifying_results)
        total_latency = sum(r.get('latency', 0) for r in qualifying_results)
        template_usage = sum(1 for r in qualifying_results if r.get('used_template', False))
        
        n_samples = len(qualifying_results)
        
        return {
            'mean_tokens': total_tokens / n_samples,
            'mean_calls': total_calls / n_samples,
            'mean_latency': total_latency / n_samples,
            'template_usage_rate': template_usage / n_samples,
            'n_samples': n_samples,
            'threshold': correctness_threshold
        }
    
    def calculate_pareto_metrics(self, baseline_results: List[Dict[str, Any]], 
                               governed_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate Pareto dominance analysis"""
        
        # Calculate mean cost and correctness for each condition
        baseline_tokens = [r.get('tokens', 0) for r in baseline_results]
        baseline_correctness = [r.get('correctness', 0) for r in baseline_results]
        governed_tokens = [r.get('tokens', 0) for r in governed_results]
        governed_correctness = [r.get('correctness', 0) for r in governed_results]
        
        baseline_mean_tokens = sum(baseline_tokens) / len(baseline_tokens) if baseline_tokens else 0
        baseline_mean_correctness = sum(baseline_correctness) / len(baseline_correctness) if baseline_correctness else 0
        governed_mean_tokens = sum(governed_tokens) / len(governed_tokens) if governed_tokens else 0
        governed_mean_correctness = sum(governed_correctness) / len(governed_correctness) if governed_correctness else 0
        
        # Calculate cost reduction and correctness delta
        cost_reduction = (baseline_mean_tokens - governed_mean_tokens) / baseline_mean_tokens if baseline_mean_tokens > 0 else 0
        correctness_delta = governed_mean_correctness - baseline_mean_correctness
        
        # Pareto dominance: governed dominates if lower cost AND higher/equal correctness
        pareto_dominates = governed_mean_tokens < baseline_mean_tokens and governed_mean_correctness >= baseline_mean_correctness
        
        # Template usage analysis
        baseline_template_rate = sum(1 for r in baseline_results if r.get('used_template', False)) / len(baseline_results) if baseline_results else 0
        governed_template_rate = sum(1 for r in governed_results if r.get('used_template', False)) / len(governed_results) if governed_results else 0
        
        return {
            'baseline_mean_tokens': baseline_mean_tokens,
            'baseline_mean_correctness': baseline_mean_correctness,
            'governed_mean_tokens': governed_mean_tokens,
            'governed_mean_correctness': governed_mean_correctness,
            'cost_reduction': cost_reduction,
            'correctness_delta': correctness_delta,
            'pareto_dominates': pareto_dominates,
            'baseline_template_rate': baseline_template_rate,
            'governed_template_rate': governed_template_rate,
            'template_rate_increase': governed_template_rate - baseline_template_rate
        }