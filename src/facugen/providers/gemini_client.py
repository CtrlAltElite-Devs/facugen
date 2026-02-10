import os
from google import genai


class GeminiClient:
    def __init__(self, model: str):
        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError(
                "GEMINI_API_KEY not set. Add it to your .env file or environment."
            )

        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.model_id = model

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config={
                "temperature": 0.9,
                "response_mime_type": "application/json",
            },
        )

        text = response.text
        return text.strip()  # ty:ignore[possibly-missing-attribute]
