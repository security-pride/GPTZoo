# GPTZoo

GPTZoo is a large-scale dataset designed to support academic research on GPTs. This repository contains 730,420 instances of GPTs, each with rich metadata, instructions, knowledge files, and information on third-party services used during its development.

To promote open research and innovation, the GPTZoo dataset will undergo continuous updates.

## Overview

GPTZoo aims to provide researchers with a comprehensive resource to study the real-world applications, performance, and potential of GPTs. The dataset includes:

- **Metadata**: 21 attributes describing each GPTs instance.
- **Instructions**: Detailed prompt instructions used to create each GPTs instance.
- **Knowledge files**: Supporting documents and files used during the development of each GPTs instance.
- **Third-party services**: Information on external services integrated with each GPTs instance.

Due to copyright and ethical considerations, we partially open access to the **instructions**, **knowledge files**, and **third-party services** data. If you require full access for scientific research purposes, please fill out the [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSfN_Mk_dgQUBXKr5_bUFCKEEgPUIvuR27EWtICESKVTOb2W9A/viewform?usp=sf_link). We will respond as soon as possible.

## Getting Started

### Prerequisites

Ensure you have the following prerequisites installed:

- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/security-pride/GPTZoo.git
cd GPTZoo
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Usage

#### Command-Line Help

The CLI supports keyword-based searching of the dataset. To use the CLI, navigate to the repository directory and run:

```bash
python gptzoo.py --help
```

#### Data Retrieval

Retrieve GPT instances based on specific criteria:

```bash
python gptzoo.py -search --tags "programming" "software guidance" --description "software development"
```

#### Data Analysis

Analyze specific subsets of the dataset:

```bash
python gptzoo.py -analyze --tags "programming" "software guidance" --description "software development"
```

## Dataset Structure

The dataset is structured as follows:

```
GPTZoo
├── automated_cli/
│      ├── data_analysis.py
│      ├── data_retrieval.py
│      └── help.py
├── crawling/
│      ├── crawl_links.py
│      ├── crawl_metadata.py
│      ├── links.txt
│      └── try_gpt_links/
├── data_processing/
│      ├── deduplication.py
│      ├── standardization.py
│      └── statistical_analysis/
│            ├── chat_count/
│            │      ├── chat_count.xlsx
│            │      └── export_chat_count.py
│            ├── description/
│            │      ├── description.py
│            │      ├── description.txt
│            │      ├── wordcloud.pdf
│            │      └── wordcloud.py
│            ├── rating/
│            └── tags/
├── dataset/
│      ├── meta_info_0.json
│      ├── meta_info_1.json
│      ├── ...
│      ├── meta_info_41.json
│      └── meta_info_42.json
├── gptzoo.py
├── requirements.txt
└── result/
```

## Contributing

We welcome contributions from the community. Please feel free to open an issue or submit a pull request.

## Acknowledgement

We would like to acknowledge [GPTs App](https://gptsapp.io/) and the [OpenAI GPT Store](https://chatgpt.com/gpts) as the sources of the data used in this project.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Citation

The collection of GPTZoo dataset relates to additional works performed by our research group. If you find GPTZoo useful, please consider citing our paper:

```
@article{zhao2024llm,
  title={LLM App Store Analysis: A Vision and Roadmap},
  author={Zhao, Yanjie and Hou, Xinyi and Wang, Shenao and Wang, Haoyu},
  journal={arXiv preprint arXiv:2404.12737},
  year={2024}
}

@article{su2024gpt,
  title={GPT Store Mining and Analysis},
  author={Su, Dongxun and Zhao, Yanjie and Hou, Xinyi and Wang, Shenao and Wang, Haoyu},
  journal={arXiv preprint arXiv:2405.10210},
  year={2024}
}

# GPTZoo bib citation here
```

