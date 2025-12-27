"""
Automated grading for refuse-or-cite test
"""
import re
from typing import Dict, Any, List, Tuple, Optional
from difflib import SequenceMatcher

class RefuseCiteGrader:
    def __init__(self):
        self.citation_pattern = r'\[CITE\s+doc:(\w+):para:(\d+)\]'
    
    def grade_response(self, question: Dict[str, Any], response: str, corpus_search_func) -> Dict[str, Any]:
        """Grade a single response"""
        
        question_id = question['question_id']
        is_answerable = question['answerable']
        
        # Check if response is a refusal
        is_refusal = self._is_refusal(response)
        
        # Extract citations
        citations = self._extract_citations(response)
        
        # Extract answer content (everything except citations)
        answer_content = self._extract_answer_content(response)
        
        if is_refusal:
            # Refusal case
            if is_answerable:
                # Should have answered but refused
                result = {
                    'question_id': question_id,
                    'response_type': 'refusal',
                    'correct_refusal': False,
                    'incorrect_refusal': True,
                    'hallucination': False,
                    'citation_accuracy': None,
                    'answer_correctness': None
                }
            else:
                # Correctly refused unanswerable question
                result = {
                    'question_id': question_id,
                    'response_type': 'refusal',
                    'correct_refusal': True,
                    'incorrect_refusal': False,
                    'hallucination': False,
                    'citation_accuracy': None,
                    'answer_correctness': None
                }
        else:
            # Answer attempt case
            if not is_answerable:
                # Answered unanswerable question - hallucination
                result = {
                    'question_id': question_id,
                    'response_type': 'answer',
                    'correct_refusal': False,
                    'incorrect_refusal': False,
                    'hallucination': True,
                    'citation_accuracy': False,
                    'answer_correctness': False
                }
            else:
                # Answerable question - check citation and content
                citation_accuracy = self._check_citation_accuracy(question, citations, corpus_search_func)
                answer_correctness = self._check_answer_correctness(question, answer_content)
                hallucination = self._check_hallucination(answer_content, citations, corpus_search_func)
                
                result = {
                    'question_id': question_id,
                    'response_type': 'answer',
                    'correct_refusal': False,
                    'incorrect_refusal': False,
                    'hallucination': hallucination,
                    'citation_accuracy': citation_accuracy,
                    'answer_correctness': answer_correctness
                }
        
        result['response'] = response
        result['citations'] = citations
        result['answer_content'] = answer_content
        
        return result
    
    def _is_refusal(self, response: str) -> bool:
        """Check if response is a refusal"""
        refusal_phrases = [
            "i can't answer",
            "cannot answer", 
            "unable to answer",
            "don't have information",
            "not available in",
            "cannot find",
            "insufficient information"
        ]
        
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in refusal_phrases)
    
    def _extract_citations(self, response: str) -> List[Dict[str, Any]]:
        """Extract citations from response"""
        citations = []
        matches = re.findall(self.citation_pattern, response)
        
        for match in matches:
            doc_id, para_idx = match
            citations.append({
                'doc_id': doc_id,
                'paragraph_idx': int(para_idx)
            })
        
        return citations
    
    def _extract_answer_content(self, response: str) -> str:
        """Extract answer content without citations"""
        # Remove citation markers
        content = re.sub(self.citation_pattern, '', response)
        # Clean up extra whitespace
        content = ' '.join(content.split())
        return content.strip()
    
    def _check_citation_accuracy(self, question: Dict[str, Any], citations: List[Dict[str, Any]], corpus_search_func) -> bool:
        """Check if citations are accurate"""
        if not citations:
            return False
        
        expected_doc_id = question['doc_id']
        expected_para_idx = question['paragraph_idx']
        
        # Check if any citation matches the expected source
        for citation in citations:
            if (citation['doc_id'] == expected_doc_id and 
                citation['paragraph_idx'] == expected_para_idx):
                return True
        
        return False
    
    def _check_answer_correctness(self, question: Dict[str, Any], answer_content: str) -> bool:
        """Check if answer content is correct"""
        expected_answer = question['answer'].lower()
        answer_lower = answer_content.lower()
        
        # Use sequence matching for fuzzy comparison
        similarity = SequenceMatcher(None, expected_answer, answer_lower).ratio()
        
        # Also check for key phrase overlap
        expected_words = set(expected_answer.split())
        answer_words = set(answer_lower.split())
        word_overlap = len(expected_words.intersection(answer_words)) / len(expected_words)
        
        # Consider correct if high similarity or good word overlap
        return similarity > 0.6 or word_overlap > 0.7
    
    def _check_hallucination(self, answer_content: str, citations: List[Dict[str, Any]], corpus_search_func) -> bool:
        """Check if answer contains hallucinated information"""
        if not citations:
            # No citations provided - assume hallucination if making factual claims
            factual_indicators = ['is', 'are', 'was', 'were', 'has', 'have', 'can', 'will']
            return any(indicator in answer_content.lower().split() for indicator in factual_indicators)
        
        # Check if answer content is supported by cited passages
        cited_text = ""
        for citation in citations:
            passage = corpus_search_func(citation['doc_id'], citation['paragraph_idx'])
            cited_text += " " + passage
        
        # Simple check: see if key claims in answer appear in cited text
        answer_words = set(answer_content.lower().split())
        cited_words = set(cited_text.lower().split())
        
        # If most answer words are not in cited text, likely hallucination
        overlap_ratio = len(answer_words.intersection(cited_words)) / len(answer_words) if answer_words else 0
        
        return overlap_ratio < 0.5  # Threshold for hallucination detection
    
    def calculate_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate aggregate metrics from grading results"""
        
        total_questions = len(results)
        answerable_questions = [r for r in results if not r.get('question', {}).get('answerable', True)]
        unanswerable_questions = [r for r in results if r.get('question', {}).get('answerable', False)]
        
        # Hallucination rate
        hallucinations = sum(1 for r in results if r.get('hallucination', False))
        hallucination_rate = hallucinations / total_questions if total_questions > 0 else 0
        
        # Citation accuracy (for answered questions with citations)
        answered_with_citations = [r for r in results if r.get('response_type') == 'answer' and r.get('citations')]
        accurate_citations = sum(1 for r in answered_with_citations if r.get('citation_accuracy', False))
        citation_accuracy = accurate_citations / len(answered_with_citations) if answered_with_citations else 0
        
        # Refusal precision/recall
        correct_refusals = sum(1 for r in results if r.get('correct_refusal', False))
        incorrect_refusals = sum(1 for r in results if r.get('incorrect_refusal', False))
        
        # Precision: correct refusals / total refusals
        total_refusals = correct_refusals + incorrect_refusals
        refusal_precision = correct_refusals / total_refusals if total_refusals > 0 else 0
        
        # Recall: correct refusals / unanswerable questions
        refusal_recall = correct_refusals / len(unanswerable_questions) if unanswerable_questions else 0
        
        return {
            'hallucination_rate': hallucination_rate,
            'citation_accuracy': citation_accuracy,
            'refusal_precision': refusal_precision,
            'refusal_recall': refusal_recall,
            'total_questions': total_questions,
            'hallucinations': hallucinations,
            'correct_refusals': correct_refusals,
            'incorrect_refusals': incorrect_refusals
        }