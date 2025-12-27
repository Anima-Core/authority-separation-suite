# Dataset Sources & Generation Notes

## Test Datasets

### Test #1: Prompt Injection
- **Source**: Single crafted document (`malicious_document.txt`)
- **Generation**: Manual creation with realistic marketing content + embedded injection
- **License**: Created for this evaluation, no external dependencies

### Test #2: Refuse-or-Cite  
- **Source**: Bundled corpus of 5 documents, 15 paragraphs
- **Generation**: Synthetic factual content covering quantum computing, ML, climate, energy, cybersecurity
- **Questions**: 7 answerable + 3 unanswerable, generated deterministically
- **License**: All content created for evaluation, no copyright issues

### Test #3: Cost-Correctness
- **Source**: 6 customer service tasks across 5 categories
- **Generation**: Synthetic workflow scenarios with template mappings
- **Templates**: 5 response templates for common inquiry types
- **License**: Created for evaluation, represents common business scenarios

### Test #4: One-Shot Constraints
- **Source**: 3 simulation environments (LavaGrid, Medication, Finance)
- **Generation**: Deterministic environments with configurable parameters
- **Episodes**: 10 episodes per environment with distribution shifts
- **License**: Simple game-like environments, no external dependencies

## Reproducibility

All datasets are:
- Generated deterministically with seed=42
- Self-contained (no external API calls)
- Documented with generation parameters
- Saved to artifacts/data/ during test runs

## Licensing

All test data is created specifically for this evaluation suite and is available under the same MIT license as the codebase. No external datasets or copyrighted content is used.