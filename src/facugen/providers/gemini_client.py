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

        # The new SDK response object has a text attribute, but let's be safe
        text = response.text
        if not text:
            # Fallback for structured responses or empty results
            try:
                text = response.candidates[0].content.parts[0].text
            except (AttributeError, IndexError):
                text = str(response)
        
        return text.strip()
