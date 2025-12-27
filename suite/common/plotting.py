"""
Plotting utilities for paper figures
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from typing import List, Dict, Any, Tuple
import numpy as np

def create_architecture_diagram(output_dir: str) -> str:
    """Create the entangled vs separated architecture diagram"""
    
    figures_dir = os.path.join(output_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Entangled architecture (top)
    ax1.set_title("Entangled: Baseline Agent", fontsize=14, fontweight='bold')
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 7)
    
    # Input box
    input_box = patches.Rectangle((0.5, 3), 1.5, 1, linewidth=2, edgecolor='black', facecolor='lightblue')
    ax1.add_patch(input_box)
    ax1.text(1.25, 3.5, 'Input', ha='center', va='center', fontweight='bold')
    
    # LLM box
    llm_box1 = patches.Rectangle((3, 3), 2, 1, linewidth=2, edgecolor='black', facecolor='lightgreen')
    ax1.add_patch(llm_box1)
    ax1.text(4, 3.5, 'LLM', ha='center', va='center', fontweight='bold')
    
    # Action box
    action_box1 = patches.Rectangle((6.5, 3), 1.5, 1, linewidth=2, edgecolor='black', facecolor='lightcoral')
    ax1.add_patch(action_box1)
    ax1.text(7.25, 3.5, 'Action', ha='center', va='center', fontweight='bold')
    
    # Arrows
    ax1.arrow(2.1, 3.5, 0.8, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
    ax1.arrow(5.1, 3.5, 1.3, 0, head_width=0.1, head_length=0.1, fc='red', ec='red', linewidth=2)
    
    # Vulnerability indicator
    ax1.text(5.7, 4.3, '⚠️ Direct\nExecution', ha='center', va='center', fontsize=10, color='red')
    
    # Authority domains
    ax1.text(5, 2.2, 'Authority over:', ha='center', va='center', fontsize=9, style='italic')
    ax1.text(5, 1.8, '• Tools • Truth • Cost • Constraints', ha='center', va='center', fontsize=8)
    
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    
    # Separated architecture (bottom)
    ax2.set_title("Separated: Governed Agent", fontsize=14, fontweight='bold')
    ax2.set_xlim(0, 12)
    ax2.set_ylim(0, 7)
    
    # Input box
    input_box2 = patches.Rectangle((0.5, 3), 1.5, 1, linewidth=2, edgecolor='black', facecolor='lightblue')
    ax2.add_patch(input_box2)
    ax2.text(1.25, 3.5, 'Input', ha='center', va='center', fontweight='bold')
    
    # LLM box
    llm_box2 = patches.Rectangle((2.5, 3), 2, 1, linewidth=2, edgecolor='black', facecolor='lightgreen')
    ax2.add_patch(llm_box2)
    ax2.text(3.5, 3.5, 'LLM', ha='center', va='center', fontweight='bold')
    
    # Boundary box
    boundary_box = patches.Rectangle((5.5, 3), 2, 1, linewidth=2, edgecolor='black', facecolor='gold')
    ax2.add_patch(boundary_box)
    ax2.text(6.5, 3.5, 'Boundary', ha='center', va='center', fontweight='bold')
    
    # Executor box
    executor_box = patches.Rectangle((8.5, 3), 1.5, 1, linewidth=2, edgecolor='black', facecolor='lightcoral')
    ax2.add_patch(executor_box)
    ax2.text(9.25, 3.5, 'Executor', ha='center', va='center', fontweight='bold')
    
    # Arrows
    ax2.arrow(2.1, 3.5, 0.3, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
    ax2.arrow(4.6, 3.5, 0.8, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
    ax2.arrow(7.6, 3.5, 0.8, 0, head_width=0.1, head_length=0.1, fc='green', ec='green')
    
    # Labels
    ax2.text(5, 4.3, 'Proposes', ha='center', va='center', fontsize=9, color='blue')
    ax2.text(8, 4.3, 'Validates', ha='center', va='center', fontsize=9, color='green')
    
    # Authority domains
    ax2.text(6.5, 2.2, 'Enforces Authority Over:', ha='center', va='center', fontsize=9, style='italic')
    ax2.text(6.5, 1.8, '• Tools • Truth • Cost • Constraints', ha='center', va='center', fontsize=8)
    
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    
    plt.tight_layout()
    
    output_path = os.path.join(figures_dir, "figure1_entangled_vs_separated.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Architecture diagram saved: {output_path}")
    return output_path

def plot_cost_correctness_curve(baseline_results: List[Dict], governed_results: List[Dict], output_dir: str) -> str:
    """Plot cost-correctness Pareto curve"""
    
    figures_dir = os.path.join(output_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    # Extract data points
    baseline_costs = [r.get('tokens', 0) for r in baseline_results]
    baseline_correctness = [r.get('correctness', 0) for r in baseline_results]
    governed_costs = [r.get('tokens', 0) for r in governed_results]
    governed_correctness = [r.get('correctness', 0) for r in governed_results]
    
    plt.figure(figsize=(8, 6))
    
    # Scatter plots
    plt.scatter(baseline_costs, baseline_correctness, alpha=0.6, label='Baseline Agent', color='red', s=50)
    plt.scatter(governed_costs, governed_correctness, alpha=0.6, label='Governed Agent', color='blue', s=50)
    
    # Mean points
    if baseline_costs and baseline_correctness:
        baseline_mean_cost = np.mean(baseline_costs)
        baseline_mean_correctness = np.mean(baseline_correctness)
        plt.scatter([baseline_mean_cost], [baseline_mean_correctness], 
                   color='darkred', s=200, marker='x', linewidth=3, label='Baseline Mean')
    
    if governed_costs and governed_correctness:
        governed_mean_cost = np.mean(governed_costs)
        governed_mean_correctness = np.mean(governed_correctness)
        plt.scatter([governed_mean_cost], [governed_mean_correctness], 
                   color='darkblue', s=200, marker='x', linewidth=3, label='Governed Mean')
    
    plt.xlabel('Cost (Tokens)', fontsize=12)
    plt.ylabel('Correctness', fontsize=12)
    plt.title('Cost-Correctness Pareto Analysis', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_path = os.path.join(figures_dir, "cost_correctness_curve.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Cost-correctness curve saved: {output_path}")
    return output_path

def plot_test_results_summary(results: List[Dict[str, Any]], output_dir: str) -> str:
    """Plot summary of all test results"""
    
    figures_dir = os.path.join(output_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    # Extract data
    test_names = []
    baseline_metrics = []
    governed_metrics = []
    
    for r in results:
        if 'error' not in r:  # Skip error results
            test_names.append(r.get('test_name', 'Unknown'))
            baseline_val = r.get('baseline', {}).get('primary_metric', 0)
            governed_val = r.get('governed', {}).get('primary_metric', 0)
            
            # Convert to float if possible
            try:
                baseline_metrics.append(float(baseline_val))
                governed_metrics.append(float(governed_val))
            except (ValueError, TypeError):
                baseline_metrics.append(0.0)
                governed_metrics.append(0.0)
    
    if not test_names:
        # No valid results to plot
        return ""
    
    # Create bar chart
    x = np.arange(len(test_names))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars1 = ax.bar(x - width/2, baseline_metrics, width, label='Baseline Agent', color='lightcoral', alpha=0.8)
    bars2 = ax.bar(x + width/2, governed_metrics, width, label='Governed Agent', color='lightblue', alpha=0.8)
    
    ax.set_xlabel('Tests', fontsize=12)
    ax.set_ylabel('Primary Metric Value', fontsize=12)
    ax.set_title('Execution Boundary Evaluation Results', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(test_names, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.annotate(f'{height:.3f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),  # 3 points vertical offset
                           textcoords="offset points",
                           ha='center', va='bottom', fontsize=9)
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    
    plt.tight_layout()
    
    output_path = os.path.join(figures_dir, "test_results_summary.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Test results summary saved: {output_path}")
    return output_path