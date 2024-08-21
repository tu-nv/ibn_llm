# Intent-based Network Configuration with LLMs
- Prepair 2 ollama servers for running embedding and main LLM
    ```bash
    CUDA_VISIBLE_DEVICES=0 OLLAMA_HOST=0.0.0.0:11434 ollama serve
    CUDA_VISIBLE_DEVICES=1 OLLAMA_HOST=0.0.0.0:11435 ollama serve
    ```
- Create a `secret.py` file for openAI API key. Can put a dummy key if do not use chatGPT.
    ```
    echo 'OPENAI_API_KEY = "key"' > secret.py
    ```
- Run evaluation
    ```
    python main.py
    ```
## Fine-tuning
- We use [unsloth](https://github.com/unslothai/unsloth) which support fine-tuning and output to ollama.
    ```
    python finetuning.py
    ```
## How to add new use case
- Make a copy of `example_use_case` then modify the files to fit your use case.
- Modify `main.py` to add new use case.
