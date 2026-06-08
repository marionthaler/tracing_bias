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
│   └── additional_data/
├── prompts/
│   ├── OLMo_base/
│   └── OLMo_instruction_tuned/
├── retrieval/
├── generation/
└── figures/
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


## Reproducing Results

The experiments in the paper use:

* 220 occupations
* Gender-identifying token lexicons
* Prompt templates
* Four decoding strategies
* OLMo 7B, OLMo 7B SFT, and OLMo 7B Instruct

## Citation

```bibtex
@inproceedings{thaler-etal-2026-how,
  title = {How Far Can Bias Go? Tracing Bias from Pre-Training Data to Alignment},
  author = {Thaler, Marion and Köksal, Abdullatif and Leidinger, Alina and Korhonen, Anna Anna and Schütze, Hinrich},
  booktitle = {Proceedings of the Fifteenth Language Resources and Evaluation Conference (LREC 2026)},
  month = {May},
  year = {2026},
  pages = {3975--3995},
  address = {Palma, Mallorca, Spain},
  publisher = {European Language Resources Association (ELRA)},
  editor = {Piperidis, Stelios and Bel, Núria and van den Heuvel, Henk and Ide, Nancy and Krek, Simon and Toral, Antonio},
  doi = {10.63317/4zeoky6waeng},
  abstract = {As LLMs are increasingly integrated into user-facing applications, addressing biases that perpetuate societal inequalities is crucial. While much work has gone into measuring and mitigating biases, fewer studies have investigated their origins. Therefore, this study examines the propagation of representational gender-occupation bias from pre-training data to LLM generations. Using zero-shot prompting and token co-occurrence analyses, we explore how biases in the pre-training data influence model generations. Our findings reveal that representational biases present in the pre-training data are amplified in the model generations, regardless of hyperparameters and prompting type. By comparing gender representation in the pre-training data with real-world distributions, our research highlights discrepancies between the data and the model, underscoring the importance of further work in mitigating bias at the data level.}
}
```

## License

Please refer to the LICENSE file for usage terms.

## Contact

For questions or issues, please open a GitHub issue or contact the authors.
