#!/usr/bin/env python3
"""
Execution Boundary Evaluation Suite
Main CLI runner for all tests
"""
import argparse
import os
import sys
import time
from typing import Dict, Any, List

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_default_config, TEST_CONFIGS
from common.logging import SuiteLogger
from common.scoreboard import generate_scoreboard
from common.plotting import create_architecture_diagram, plot_test_results_summary

# Import test runners
from tests.test1_prompt_injection.runner import run_test as run_test1
from tests.test2_refuse_or_cite.runner import run_test as run_test2
from tests.test3_cost_correctness.runner import run_test as run_test3
from tests.test4_one_shot_constraints.runner import run_test as run_test4

def run_single_test(test_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single test by name"""
    
    test_runners = {
        'test1': run_test1,
        'test2': run_test2,
        'test3': run_test3,
        'test4': run_test4
    }
    
    test_display_names = {
        'test1': 'Tool Authority (Prompt Injection)',
        'test2': 'Epistemic Authority (Refuse-or-Cite)', 
        'test3': 'Execution Authority (Cost-Correctness)',
        'test4': 'Temporal Authority (One-Shot Constraints)'
    }
    
    if test_name not in test_runners:
        raise ValueError(f"Unknown test: {test_name}")
    
    print(f"\n{'='*60}")
    print(f" Running {test_display_names.get(test_name, test_name)}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    # Convert config object to dict
    config_dict = {
        'output_dir': config.output_dir,
        'seed': config.seed,
        'quick_mode': config.quick_mode,
        'model_provider': config.model_provider
    }
    
    result = test_runners[test_name](config_dict)
    end_time = time.time()
    
    result['runtime_seconds'] = end_time - start_time
    
    print(f"✅ {test_name} completed in {result['runtime_seconds']:.1f}s")
    return result

def run_all_tests(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run all enabled tests"""
    
    results = []
    
    # Convert config object to dict
    config_dict = {
        'output_dir': config.output_dir,
        'seed': config.seed,
        'quick_mode': config.quick_mode,
        'model_provider': config.model_provider
    }
    
    # Test 1: Prompt Injection
    if config.test1_enabled:
        try:
            result = run_single_test('test1', config)
            results.append(result)
        except Exception as e:
            print(f"❌ Test 1 failed: {e}")
            results.append({
                "test_name": "Prompt Injection",
                "error": str(e),
                "baseline": {"primary_metric": "ERROR"},
                "governed": {"primary_metric": "ERROR"}
            })
    
    # Test 2: Refuse-or-Cite
    if config.test2_enabled:
        try:
            result = run_single_test('test2', config)
            results.append(result)
        except Exception as e:
            print(f"❌ Test 2 failed: {e}")
            results.append({
                "test_name": "Refuse-or-Cite",
                "error": str(e),
                "baseline": {"primary_metric": "ERROR"},
                "governed": {"primary_metric": "ERROR"}
            })
    
    # Test 3: Cost-Correctness
    if config.test3_enabled:
        try:
            result = run_single_test('test3', config)
            results.append(result)
        except Exception as e:
            print(f"❌ Test 3 failed: {e}")
            results.append({
                "test_name": "Cost-Correctness",
                "error": str(e),
                "baseline": {"primary_metric": "ERROR"},
                "governed": {"primary_metric": "ERROR"}
            })
    
    # Test 4: One-Shot Constraints
    if config.test4_enabled:
        try:
            result = run_single_test('test4', config)
            results.append(result)
        except Exception as e:
            print(f"❌ Test 4 failed: {e}")
            results.append({
                "test_name": "One-Shot Constraints",
                "error": str(e),
                "baseline": {"primary_metric": "ERROR"},
                "governed": {"primary_metric": "ERROR"}
            })
    
    return results

def generate_artifacts(results: List[Dict[str, Any]], config):
    """Generate paper-ready artifacts"""
    
    print(f"\n{'='*60}")
    print(" Generating Artifacts")
    print(f"{'='*60}")
    
    output_dir = config.output_dir
    
    # Generate scoreboard
    print("📊 Generating scoreboard...")
    scoreboard_path = generate_scoreboard(results, output_dir)
    
    # Generate figures
    print("📈 Generating figures...")
    
    # Architecture diagram
    arch_diagram = create_architecture_diagram(output_dir)
    
    # Test results summary
    summary_plot = plot_test_results_summary(results, output_dir)
    
    print(f"✅ Artifacts generated in {output_dir}/")
    print(f"   - Scoreboard: {scoreboard_path}")
    print(f"   - Architecture: {arch_diagram}")
    print(f"   - Summary: {summary_plot}")

def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(
        description="Authority Separation Evaluation Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m suite.run --all                    # Run all evaluations
  python -m suite.run --test test1             # Run tool authority evaluation
  python -m suite.run --test test2 --quick     # Run epistemic authority evaluation (quick mode)
  python -m suite.run --all --output results/  # Run all evaluations with custom output dir
        """
    )
    
    parser.add_argument('--all', action='store_true', 
                       help='Run all evaluations')
    parser.add_argument('--test', choices=['test1', 'test2', 'test3', 'test4'],
                       help='Run specific evaluation (test1=Tool Authority, test2=Epistemic Authority, test3=Execution Authority, test4=Temporal Authority)')
    parser.add_argument('--quick', action='store_true',
                       help='Quick mode (smaller datasets)')
    parser.add_argument('--output', default='artifacts',
                       help='Output directory for results')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for reproducibility (default: 42)')
    parser.add_argument('--model', choices=['mock', 'openai', 'anthropic'], default='mock',
                       help='Model provider to use (default: mock for reproducibility)')
    
    args = parser.parse_args()
    
    if not args.all and not args.test:
        parser.error("Must specify either --all or --test")
    
    # Setup configuration
    config = get_default_config()
    config.quick_mode = args.quick
    config.output_dir = args.output
    config.seed = args.seed
    config.model_provider = args.model
    
    # Create output directory
    os.makedirs(config.output_dir, exist_ok=True)
    
    print("🔬 Authority Separation Evaluation Suite")
    print(f"   Mode: {'Quick' if config.quick_mode else 'Full'}")
    print(f"   Model: {config.model_provider}")
    print(f"   Seed: {config.seed} (deterministic)")
    print(f"   Output: {config.output_dir}")
    
    start_time = time.time()
    
    try:
        if args.all:
            # Run all tests
            results = run_all_tests(config)
        else:
            # Run single test
            result = run_single_test(args.test, config)
            results = [result]
        
        # Generate artifacts
        generate_artifacts(results, config)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n🎉 Suite completed in {total_time:.1f}s")
        
        # Print summary
        print(f"\n📋 Results Summary:")
        for result in results:
            test_name = result.get('test_name', 'Unknown')
            baseline_metric = result.get('baseline', {}).get('primary_metric', 'N/A')
            governed_metric = result.get('governed', {}).get('primary_metric', 'N/A')
            
            if 'error' in result:
                print(f"   ❌ {test_name}: ERROR - {result['error']}")
            else:
                print(f"   ✅ {test_name}: {baseline_metric} → {governed_metric}")
        
        print(f"\n📁 Full results available in: {config.output_dir}/")
        
    except KeyboardInterrupt:
        print("\n⚠️  Suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Suite failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()