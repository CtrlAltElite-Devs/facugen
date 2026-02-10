# FacuGen

Dataset generator CLI for multilingual student feedback. Generate high-quality, synthetic datasets for training and evaluating sentiment analysis models in various Philippine languages and dialects.

## Features

- **Multilingual Support**: Supports English, Tagalog, Cebuano, Taglish, and Cebuano-English mix.
- **Multiple Providers**: Integration with OpenAI, Google Gemini, and local models via **Ollama**.
- **Sync & Async Generation**: Fast concurrent generation using `asyncio`.
- **Balanced Sampling**: Option to generate equal distributions of sentiment labels.
- **Progress Tracking**: Built-in `tqdm` support for monitoring generation.

## Installation

Ensure you have [uv](https://github.com/astral-sh/uv) installed.

```bash
git clone https://github.com/CtrlAltElite-Devs/facugen.git
cd facugen
uv sync
```

## Configuration

### Cloud Providers
Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
```

### Local Models (Ollama)
Ensure [Ollama](https://ollama.com/) is installed and running on your machine. No API key is required for local models.

## Usage

### Basic Generation
```bash
uv run facugen generate --lang taglish --count 100
```

### Local Generation (Ollama)
Pull your desired model first:
```bash
ollama pull qwen2.5:7b
```

Run generation using the local model:
```bash
uv run facugen generate --lang tagalog --count 50 --model qwen2.5:7b
```

### Advanced Options
```bash
uv run facugen generate \
  --lang cebu_eng_mix \
  --count 30 \
  --model gpt-4o-mini \
  --balance-labels \
  --seed 42 \
  --async \
  --concurrency 5 \
  --out datasets/feedback.jsonl
```

### Command Arguments
- `--lang`: Target language (choices: `cebu_eng_mix`, `cebuano`, `english`, `tagalog`, `taglish`).
- `--count`: Number of samples to generate.
- `--model`: Model to use (e.g., `gpt-4o`, `gemini-1.5-flash`, `qwen2.5:7b`).
- `--out`: Output path for JSONL file (default: `out/dataset.jsonl`).
- `--balance-labels`: Ensures equal distribution of positive, neutral, and negative sentiments.
- `--seed`: Set a random seed for reproducible dataset generation.
- `--async`: Enables concurrent requests for much faster generation.
- `--concurrency`: Max number of parallel requests (default: 5). **Recommended value is 5** to avoid aggressive rate limiting from providers.

## Important: Model Limitations

> [!WARNING]
> **Gemini Model Support**: Currently, Gemini models are more limited in features compared to OpenAI models within this CLI:
> - **Rate Limiting**: Gemini free-tier models (like `gemini-2.5-flash-lite`) have very strict quotas (e.g., 20 requests per day).
> - **Stability**: You may encounter more frequent `RESOURCE_EXHAUSTED` errors with Gemini. The CLI implements exponential backoff, but large batches may still fail if daily quotas are reached.
> - **Inference Speed**: In concurrent mode, Gemini models might throttle more aggressively than OpenAI.

## License

MIT
