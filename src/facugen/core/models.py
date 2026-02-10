from dataclasses import dataclass


@dataclass(frozen=True)
class ModelSpec:
    provider: str
    model: str


SUPPORTED_MODELS = {
    # OpenAI
    "gpt-4.1-mini": ModelSpec(provider="openai", model="gpt-4.1-mini"),
    "gpt-4o-mini": ModelSpec(provider="openai", model="gpt-4o-mini"),
    # Gemini
    "gemini-1.5-flash": ModelSpec(provider="gemini", model="gemini-1.5-flash"),
    "gemini-1.5-pro": ModelSpec(provider="gemini", model="gemini-1.5-pro"),
    "gemini-2.5-flash-lite": ModelSpec(
        provider="gemini", model="gemini-2.5-flash-lite"
    ),
    # Ollama (Local)
    "llama3.2": ModelSpec(provider="ollama", model="llama3.2"),
    "llama3.2:1b": ModelSpec(provider="ollama", model="llama3.2:1b"),
    "mistral": ModelSpec(provider="ollama", model="mistral"),
    "gemma2": ModelSpec(provider="ollama", model="gemma2"),
    "qwen2.5": ModelSpec(provider="ollama", model="qwen2.5"),
    "qwen2.5:3b": ModelSpec(provider="ollama", model="qwen2.5:3b"),
    "qwen2.5:7b": ModelSpec(provider="ollama", model="qwen2.5:7b"),
}
