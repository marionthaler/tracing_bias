# Tracing Bias: From Pre-Training Data to Alignment

Code accompanying the paper:

**How Far Can Bias Go? Tracing Bias from Pre-Training Data to Alignment**
Marion Thaler, Abdullatif Köksal, Alina Leidinger, Anna Korhonen, and Hinrich Schütze
LREC-COLING 2026

## Overview

This repository contains the code used to analyze how representational gender-occupation bias propagates from large language model pre-training data into model outputs.

Using the fully open OLMo ecosystem and the Dolma pre-training corpus, we investigate:

* Gender-occupation associations in pre-training data
* Gender-occupation associations in generated model outputs
* Bias amplification and de-amplification during generation
* Correlations between data-level and model-level bias
* The effect of instruction tuning and alignment on bias

Our experiments compare:

* OLMo 7B (Base)
* OLMo 7B SFT
* OLMo 7B Instruct

across multiple prompting strategies and decoding configurations.

## Main Findings

* Gender representation in Dolma is strongly imbalanced across occupations.
* Biases present in pre-training data are reflected in model outputs.
* The OLMo 7B base model tends to amplify the under-representation of women.
* Instruction tuning reduces representation bias but does not eliminate stereotypical occupational associations.
* Bias patterns remain robust across prompting styles and decoding strategies.

## Repository Structure

```text
.
├── data/
│   ├── occupations/
│   ├── gender_terms/
│   └── statistics/
├── prompts/
│   ├── neutral/
│   ├── positive/
│   └── negative/
├── retrieval/
│   ├── dolma_queries/
│   └── cooccurrence_analysis/
├── generation/
│   ├── olmo_base/
│   ├── olmo_sft/
│   └── olmo_instruct/
├── evaluation/
│   ├── sta/
│   ├── amplification/
│   └── correlation/
├── figures/
├── notebooks/
└── scripts/
```

## Methodology

### 1. Dataset Analysis

We retrieve documents from the Dolma corpus containing occupational terms and compute co-occurrences between occupations and gender-identifying terms.

### 2. Model Generation

For each occupation, we generate responses using:

* Neutral prompts
* Positive prompts
* Negative prompts

under multiple decoding configurations:

* Baseline
* Top-k sampling
* Top-p sampling
* Temperature sampling

### 3. Bias Evaluation

We evaluate:

#### Stereotypical Association (STA)

Measures deviation from a reference gender distribution.

#### Bias Amplification

Measures whether model outputs amplify or reduce gender imbalances present in pre-training data.

#### Correlation Analysis

Measures the relationship between gender distributions in the training data and generated outputs.

## Installation

```bash
git clone https://github.com/marionthaler/tracing_bias.git
cd tracing_bias

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Running the Experiments

### Analyze Dolma Co-occurrences

```bash
python scripts/analyze_dolma.py
```

### Generate Model Outputs

```bash
python scripts/generate.py \
    --model olmo-7b \
    --prompt_type neutral \
    --decoding baseline
```

### Compute Bias Metrics

```bash
python scripts/evaluate.py
```

## Reproducing Results

The experiments in the paper use:

* 220 occupations
* Gender-identifying token lexicons
* Multiple prompt templates
* Four decoding strategies
* OLMo 7B, OLMo 7B SFT, and OLMo 7B Instruct

Detailed configurations can be found in the `configs/` directory.

## Citation

```bibtex
@inproceedings{thaler2026tracingbias,
  title={How Far Can Bias Go? Tracing Bias from Pre-Training Data to Alignment},
  author={Thaler, Marion and Köksal, Abdullatif and Leidinger, Alina and Korhonen, Anna and Schütze, Hinrich},
  booktitle={Proceedings of the Fifteenth Language Resources and Evaluation Conference (LREC-COLING 2026)},
  year={2026}
}
```

## License

Please refer to the LICENSE file for usage terms.

## Contact

For questions or issues, please open a GitHub issue or contact the authors.
