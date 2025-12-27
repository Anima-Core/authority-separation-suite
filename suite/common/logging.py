"""
Structured logging for the evaluation suite
"""
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List

class SuiteLogger:
    def __init__(self, output_dir: str, test_name: str):
        self.output_dir = output_dir
        self.test_name = test_name
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        self.log_dir = os.path.join(output_dir, "results", f"{test_name}_{self.run_id}")
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger(f"suite.{test_name}")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        log_file = os.path.join(self.log_dir, "run.log")
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
        # Data storage
        self.results = []
        self.tool_calls = []
        self.boundary_decisions = []
    
    def log_result(self, item_id: str, result: Dict[str, Any]):
        """Log a single test result"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "item_id": item_id,
            "result": result
        }
        self.results.append(entry)
        self.logger.info(f"Result {item_id}: {result}")
    
    def log_tool_call(self, agent_type: str, tool_name: str, args: Dict[str, Any], result: Any):
        """Log a tool call"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_type": agent_type,
            "tool_name": tool_name,
            "args": args,
            "result": str(result)[:500]  # Truncate long results
        }
        self.tool_calls.append(entry)
        self.logger.info(f"Tool call [{agent_type}]: {tool_name}({args}) -> {str(result)[:100]}")
    
    def log_boundary_decision(self, tool_name: str, args: Dict[str, Any], authorized: bool, reason: str):
        """Log an execution boundary decision"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "args": args,
            "authorized": authorized,
            "reason": reason
        }
        self.boundary_decisions.append(entry)
        self.logger.info(f"Boundary decision: {tool_name}({args}) -> {'ALLOWED' if authorized else 'DENIED'}: {reason}")
    
    def save_results(self):
        """Save all logged data to files"""
        # Save results
        results_file = os.path.join(self.log_dir, "results.jsonl")
        with open(results_file, 'w') as f:
            for result in self.results:
                f.write(json.dumps(result) + '\n')
        
        # Save tool calls
        tools_file = os.path.join(self.log_dir, "tool_calls.jsonl")
        with open(tools_file, 'w') as f:
            for call in self.tool_calls:
                f.write(json.dumps(call) + '\n')
        
        # Save boundary decisions
        boundary_file = os.path.join(self.log_dir, "boundary_decisions.jsonl")
        with open(boundary_file, 'w') as f:
            for decision in self.boundary_decisions:
                f.write(json.dumps(decision) + '\n')
        
        self.logger.info(f"Results saved to {self.log_dir}")
        return self.log_dir