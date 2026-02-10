import ollama
from facugen.providers.base import LLMProvider


class OllamaClient(LLMProvider):
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                format="json",  # Enforce JSON output for structured generation
                options={
                    "temperature": 0.9,
                },
            )
            return response["message"]["content"]
        except ollama.ResponseError as e:
            if e.status_code == 404:
                raise RuntimeError(
                    f"Model '{self.model}' not found in Ollama. "
                    f"Please run 'ollama pull {self.model}' to download it."
                ) from e
            raise
