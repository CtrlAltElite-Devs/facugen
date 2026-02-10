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
}
