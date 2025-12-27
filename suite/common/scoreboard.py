"""
Scoreboard generation for unified results
"""
import os
import csv
from typing import List, Dict, Any
from datetime import datetime

def generate_scoreboard(results: List[Dict[str, Any]], output_dir: str) -> str:
    """Generate unified scoreboard in CSV and Markdown formats"""
    
    # Ensure output directories exist
    tables_dir = os.path.join(output_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare data for table
    rows = []
    for result in results:
        test_name = result.get('test_name', 'Unknown')
        baseline_metric = result.get('baseline', {}).get('primary_metric', 'N/A')
        governed_metric = result.get('governed', {}).get('primary_metric', 'N/A')
        
        # Calculate improvement
        if isinstance(baseline_metric, (int, float)) and isinstance(governed_metric, (int, float)):
            if baseline_metric == 0:
                improvement = "N/A"
            else:
                # For rates (lower is better), calculate reduction
                if test_name in ["Prompt Injection", "Refuse-or-Cite", "One-Shot Constraints"]:
                    improvement = f"{((baseline_metric - governed_metric) / baseline_metric * 100):.1f}%"
                else:
                    # For cost metrics, show reduction
                    improvement = f"{((baseline_metric - governed_metric) / baseline_metric * 100):.1f}%"
        else:
            improvement = "N/A"
        
        rows.append({
            'Test': test_name,
            'Metric': result.get('metric_name', 'Unknown'),
            'Baseline': baseline_metric,
            'Governed': governed_metric,
            'Improvement': improvement,
            'Notes': result.get('notes', '')
        })
    
    # Write CSV
    csv_path = os.path.join(tables_dir, "scoreboard.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Test', 'Metric', 'Baseline', 'Governed', 'Improvement', 'Notes'])
        writer.writeheader()
        writer.writerows(rows)
    
    # Write Markdown
    md_path = os.path.join(tables_dir, "scoreboard.md")
    with open(md_path, 'w') as f:
        f.write("# Authority Separation Evaluation Results\n\n")
        f.write(f"Generated: {timestamp}\n\n")
        
        f.write("## Threat Model & Assumptions\n\n")
        f.write("This evaluation demonstrates execution authority separation under controlled conditions:\n\n")
        f.write("- **Attacker Model**: Adversary controls inputs but not code or policies\n")
        f.write("- **Policy Stability**: Authority policies remain static during evaluation\n") 
        f.write("- **Boundary Trust**: Execution boundary implementation is trusted\n")
        f.write("- **Executor Separation**: Tool execution occurs outside the language model\n")
        f.write("- **Evaluation Scope**: Architectural principle demonstration, not comprehensive security analysis\n\n")
        
        f.write("## Summary\n\n")
        f.write("| Test | Metric | Baseline | Governed | Improvement | Notes |\n")
        f.write("|------|--------|----------|----------|-------------|-------|\n")
        
        for row in rows:
            f.write(f"| {row['Test']} | {row['Metric']} | {row['Baseline']} | {row['Governed']} | {row['Improvement']} | {row['Notes']} |\n")
        
        f.write("\n## Evaluation Descriptions\n\n")
        f.write("Each evaluation demonstrates the same architectural principle across different failure domains:\n\n")
        f.write("- **Tool Authority**: Tool authority failure - unauthorized tool execution\n")
        f.write("- **Epistemic Authority**: Epistemic authority failure - unsupported factual claims\n") 
        f.write("- **Execution Authority**: Execution authority misuse - inefficient resource usage\n")
        f.write("- **Temporal Authority**: Temporal authority failure - repeated catastrophic actions\n\n")
        
        f.write("## Architecture\n\n")
        f.write("**Baseline Agent**: Language model can call tools directly using tool wrappers with prompt-based security rules only.\n\n")
        f.write("**Governed Agent**: Same language model and prompts, but ALL tool calls must go through execution boundary policy checks. Language model can only propose tool calls; boundary approves/denies.\n\n")
        
        f.write("**Key Principle**: Same agent, same task, same input - only authority placement changes.\n\n")
    
    print(f"Scoreboard generated: {csv_path} and {md_path}")
    return md_path