# **KARMA: Augmenting Embodied AI Agents with Long-and-short Term Memory Systems**

This repository contains the code for KARMA, an embodied AI agent framework augmented with long-and-short term memory systems.

## Setup

To get started, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Sonhoangvo/karma-with-fb
    cd karma-with-fb
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv karma-venv
    source karma-venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## OpenAI API Key Configuration
The project relies on the OpenAI API for its Language Model functionalities.

1.  **Obtain an API Key:** Create an API Key at [https://platform.openai.com/](https://platform.openai.com/).

2.  **Configure API Key in `llm_as_planner.py`:**
    Open `scripts/llm_as_planner.py` and replace `'sk-or-v1-...'` with your actual OpenAI API key:
    ```python
    # File: scripts/llm_as_planner.py
    openai.api_key = "YOUR_OPENAI_API_KEY_HERE"
    ```

3.  **Configure API Key in `execute_LLM_plan.py`:**
    Open `scripts/execute_LLM_plan.py` and replace `'sk-or-v1-...'` with your actual OpenAI API key:
    ```python
    # File: scripts/execute_LLM_plan.py
    api_key = "YOUR_OPENAI_API_KEY_HERE"
    ```

## Running the GUI Application
Run the following command to launch the GUI and interact with the KARMA agent:

```bash
./karma-venv/bin/python -m scripts.GUI_karma 
```
Note: You can enter the tasks you want the agent to perform in the GUI, for example: "wash an apple and put it on the countertop", "slice an apple and place it on the plate".

## Citation
If you find our paper and code useful in your research, please consider giving a star ⭐ and citation 📝:

```
@article{wang2024karma,
  title={Karma: Augmenting embodied ai agents with long-and-short term memory systems},
  author={Wang, Zixuan and Yu, Bo and Zhao, Junzhe and Sun, Wenhao and Hou, Sai and Liang, Shuai and Hu, Xing and Han, Yinhe and Gan, Yiming},
  journal={arXiv preprint arXiv:2409.14908},
  year={2024}
}
```