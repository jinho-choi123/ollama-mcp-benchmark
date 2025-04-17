
## Description
LLM Client that acts as a MCP Client. To check the GPU usage, we are running whole model in the local.

## Prerequisties
- Install [Ollama](https://ollama.com/download/linux)
- Setup python environment using [uv-python](https://github.com/astral-sh/uv)

## Getting Started
1. Run the Ollama app
```bash
$ ollama serve
```
2. Install the model weights(gemma3:12b by default)
```bash
$ ollama pull gemma3:12b
```
3. Run the MCP client.
```bash
$ uv run main.py
```
4. Have fun!
