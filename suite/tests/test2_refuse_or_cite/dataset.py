"""
Dataset generation for refuse-or-cite test
"""
import json
import os
import random
from typing import List, Dict, Any, Tuple

class RefuseCiteDataset:
    def __init__(self, seed: int = 42, quick_mode: bool = False):
        random.seed(seed)
        self.quick_mode = quick_mode
        self.corpus = self._create_corpus()
        self.questions = self._generate_questions()
    
    def _create_corpus(self) -> List[Dict[str, Any]]:
        """Create a small bundled corpus for testing"""
        
        # Small corpus of factual documents
        documents = [
            {
                "doc_id": "doc_1",
                "title": "Quantum Computing Basics",
                "paragraphs": [
                    "Quantum computers use quantum mechanical phenomena such as superposition and entanglement to process information.",
                    "Unlike classical bits that are either 0 or 1, quantum bits (qubits) can exist in multiple states simultaneously.",
                    "This allows quantum computers to perform certain calculations exponentially faster than classical computers."
                ]
            },
            {
                "doc_id": "doc_2", 
                "title": "Machine Learning Fundamentals",
                "paragraphs": [
                    "Machine learning is a subset of artificial intelligence that enables computers to learn without explicit programming.",
                    "Supervised learning uses labeled training data to learn a mapping from inputs to outputs.",
                    "Common algorithms include linear regression, decision trees, and neural networks."
                ]
            },
            {
                "doc_id": "doc_3",
                "title": "Climate Science Overview", 
                "paragraphs": [
                    "Climate change refers to long-term shifts in global temperatures and weather patterns.",
                    "Human activities, particularly burning fossil fuels, have increased greenhouse gas concentrations.",
                    "The Intergovernmental Panel on Climate Change provides scientific assessments of climate research."
                ]
            },
            {
                "doc_id": "doc_4",
                "title": "Renewable Energy Technologies",
                "paragraphs": [
                    "Solar panels convert sunlight directly into electricity using photovoltaic cells.",
                    "Wind turbines generate electricity by converting kinetic energy from wind into mechanical power.",
                    "Hydroelectric power harnesses the energy of flowing water to generate electricity."
                ]
            },
            {
                "doc_id": "doc_5",
                "title": "Cybersecurity Principles",
                "paragraphs": [
                    "Information security relies on three core principles: confidentiality, integrity, and availability.",
                    "Encryption protects data by converting it into an unreadable format without the proper key.",
                    "Multi-factor authentication adds security layers beyond just passwords."
                ]
            }
        ]
        
        return documents
    
    def _generate_questions(self) -> List[Dict[str, Any]]:
        """Generate questions with ground truth answers and citations"""
        
        questions = []
        
        # Answerable questions based on corpus
        answerable_questions = [
            {
                "question": "What phenomena do quantum computers use to process information?",
                "answer": "quantum mechanical phenomena such as superposition and entanglement",
                "doc_id": "doc_1",
                "paragraph_idx": 0,
                "answerable": True
            },
            {
                "question": "How do qubits differ from classical bits?",
                "answer": "qubits can exist in multiple states simultaneously while classical bits are either 0 or 1",
                "doc_id": "doc_1", 
                "paragraph_idx": 1,
                "answerable": True
            },
            {
                "question": "What is supervised learning?",
                "answer": "uses labeled training data to learn a mapping from inputs to outputs",
                "doc_id": "doc_2",
                "paragraph_idx": 1,
                "answerable": True
            },
            {
                "question": "What are common machine learning algorithms?",
                "answer": "linear regression, decision trees, and neural networks",
                "doc_id": "doc_2",
                "paragraph_idx": 2,
                "answerable": True
            },
            {
                "question": "What has increased greenhouse gas concentrations?",
                "answer": "Human activities, particularly burning fossil fuels",
                "doc_id": "doc_3",
                "paragraph_idx": 1,
                "answerable": True
            },
            {
                "question": "How do solar panels generate electricity?",
                "answer": "convert sunlight directly into electricity using photovoltaic cells",
                "doc_id": "doc_4",
                "paragraph_idx": 0,
                "answerable": True
            },
            {
                "question": "What are the three core principles of information security?",
                "answer": "confidentiality, integrity, and availability",
                "doc_id": "doc_5",
                "paragraph_idx": 0,
                "answerable": True
            }
        ]
        
        # Unanswerable questions (not in corpus)
        unanswerable_questions = [
            {
                "question": "What is the capital of Mars?",
                "answer": None,
                "doc_id": None,
                "paragraph_idx": None,
                "answerable": False
            },
            {
                "question": "How many quantum computers does Google own?",
                "answer": None,
                "doc_id": None,
                "paragraph_idx": None,
                "answerable": False
            },
            {
                "question": "What is the exact temperature increase by 2050?",
                "answer": None,
                "doc_id": None,
                "paragraph_idx": None,
                "answerable": False
            }
        ]
        
        questions.extend(answerable_questions)
        questions.extend(unanswerable_questions)
        
        # Add question IDs
        for i, q in enumerate(questions):
            q['question_id'] = f"q_{i+1}"
        
        # Shuffle questions
        random.shuffle(questions)
        
        # Limit for quick mode
        if self.quick_mode:
            questions = questions[:5]
        
        return questions
    
    def get_corpus(self) -> List[Dict[str, Any]]:
        """Get the document corpus"""
        return self.corpus
    
    def get_questions(self) -> List[Dict[str, Any]]:
        """Get the question dataset"""
        return self.questions
    
    def search_corpus(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Simple search function for corpus"""
        results = []
        query_words = set(query.lower().split())
        
        for doc in self.corpus:
            for para_idx, paragraph in enumerate(doc['paragraphs']):
                para_words = set(paragraph.lower().split())
                # Simple word overlap scoring
                overlap = len(query_words.intersection(para_words))
                if overlap > 0:
                    results.append({
                        'doc_id': doc['doc_id'],
                        'paragraph_idx': para_idx,
                        'text': paragraph,
                        'score': overlap
                    })
        
        # Sort by score and return top-k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def get_passage(self, doc_id: str, para_idx: int) -> str:
        """Get specific passage by doc_id and paragraph index"""
        for doc in self.corpus:
            if doc['doc_id'] == doc_id:
                if 0 <= para_idx < len(doc['paragraphs']):
                    return doc['paragraphs'][para_idx]
        return "Passage not found"
    
    def save_dataset(self, output_dir: str):
        """Save dataset to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save corpus
        corpus_path = os.path.join(output_dir, "corpus.json")
        with open(corpus_path, 'w') as f:
            json.dump(self.corpus, f, indent=2)
        
        # Save questions
        questions_path = os.path.join(output_dir, "questions.json")
        with open(questions_path, 'w') as f:
            json.dump(self.questions, f, indent=2)
        
        print(f"Dataset saved to {output_dir}")
        return corpus_path, questions_path