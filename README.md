# Authority Separation in AI Systems: Evaluation Suite

This repository provides the reproducible evaluation suite supporting the results in "Authority Separation in AI Systems: Structural Guarantees Across Security, Epistemics, Economics, and Safety."

## Overview

Authority separation addresses execution entanglement—the direct coupling of language model reasoning with action execution—which creates systematic vulnerabilities across multiple domains. This suite demonstrates that separating proposal generation from execution authority provides structural guarantees where prompt-based approaches exhibit persistent failures.

## Architecture

The evaluation compares two agent architectures across four domains:

- **Baseline Agent**: Language model directly executes tools with prompt-based security rules
- **Governed Agent**: Language model proposes actions; execution boundary validates against authority policies

**Key Principle**: Same agent, same task, same input—only authority placement changes.

## Evaluations

This suite contains four complementary evaluations demonstrating authority separation across different failure domains:

### 1. Tool Authority (Prompt Injection)
- **Domain**: Security - unauthorized tool execution
- **Threat**: Embedded instructions cause agents to execute out-of-scope tools
- **Metric**: Unauthorized tool invocation rate
- **Result**: Baseline exhibits systematic tool authority violations; governed agent maintains authorization boundaries

### 2. Epistemic Authority (Refuse-or-Cite)
- **Domain**: Knowledge - unsupported factual claims  
- **Threat**: Agents make assertions without supporting evidence
- **Metric**: Hallucination rate (claims without citation support)
- **Result**: Baseline generates unsupported claims; governed agent enforces evidence requirements

### 3. Execution Authority (Cost-Correctness)
- **Domain**: Economics - inefficient resource usage
- **Threat**: Agents choose expensive generation over efficient structured alternatives
- **Metric**: Computational cost at fixed correctness threshold
- **Result**: Baseline defaults to expensive generation; governed agent prefers efficient templates

### 4. Temporal Authority (One-Shot Constraints)
- **Domain**: Safety - repeated catastrophic actions
- **Threat**: Agents repeat dangerous actions across episodes despite prior failures
- **Metric**: Catastrophic actions after initial learning event
- **Result**: Baseline repeats failures; governed agent maintains constraint memory

## Reproducibility

### Requirements
```bash
pip install -r requirements.txt
```

### Running Evaluations
```bash
# Run all evaluations
python -m suite.run --all

# Run individual evaluation
python -m suite.run --test test1  # Tool Authority
python -m suite.run --test test2  # Epistemic Authority  
python -m suite.run --test test3  # Execution Authority
python -m suite.run --test test4  # Temporal Authority

# Quick mode (smaller datasets)
python -m suite.run --all --quick
```

### Outputs
- **Scoreboard**: `artifacts/tables/scoreboard.md` and `scoreboard.csv`
- **Figures**: `artifacts/figures/` (architecture diagrams, result summaries)
- **Detailed Logs**: `artifacts/results/` (per-evaluation execution traces)

### Deterministic Execution
All evaluations use deterministic datasets and mock language model responses (seed=42) for reproducible results. Real language model integration is supported but not required for replication.

## Distinction from Minimal Demo

This repository contains both:
1. **Original 5-minute demo** (`run_demo.py`) - Single prompt injection scenario
2. **Complete evaluation suite** (`suite/`) - Four-domain authority separation analysis

The evaluation suite provides comprehensive evidence for the paper's claims across multiple domains, while the demo offers a focused illustration of the core principle.

## Repository Structure

```
authority-separation-suite/
├── README.md                    # This file
├── requirements.txt             # Dependencies
├── LICENSE                      # MIT license
├── run_demo.py                  # Original prompt injection demo
├── malicious_document.txt       # Demo input data
├── policy.yaml                  # Demo execution boundary policy
├── baseline_agent.py            # Demo baseline implementation
├── governed_agent.py            # Demo governed implementation
│
├── suite/                       # Evaluation suite
│   ├── run.py                   # Main CLI entry point
│   ├── config.py                # Shared configuration
│   ├── common/                  # Shared utilities
│   │   ├── logging.py           # Structured evaluation logging
│   │   ├── metrics.py           # Metric calculation
│   │   ├── models.py            # Mock LM and execution boundary
│   │   ├── scoreboard.py        # Result aggregation
│   │   └── plotting.py          # Figure generation
│   └── tests/                   # Individual evaluations
│       ├── test1_prompt_injection/    # Tool Authority
│       ├── test2_refuse_or_cite/      # Epistemic Authority
│       ├── test3_cost_correctness/    # Execution Authority
│       └── test4_one_shot_constraints/ # Temporal Authority
│
└── artifacts/                   # Generated outputs (created on run)
    ├── figures/                 # Paper figures
    ├── tables/                  # Result tables
    └── results/                 # Detailed logs
```

## Citation

If you use this evaluation suite in your research, please cite:

```bibtex
@article{authority-separation-2024,
  title={Authority Separation in AI Systems: Structural Guarantees Across Security, Epistemics, Economics, and Safety},
  author={[Author Name]},
  journal={[Journal Name]},
  year={2024}
}
```

## License

MIT License - see LICENSE file for details.