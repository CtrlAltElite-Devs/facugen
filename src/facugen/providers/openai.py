import os
from openai import OpenAI


class OpenAIClient:
    def __init__(self, model: str):
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY not set.Add it to your .env file or environment"
            )

        self.model = model
        self.client = OpenAI()

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            response_format={"type": "json_object"},
        )

        return response.choices[0].message.content.strip()  # ty:ignore[possibly-missing-attribute]
