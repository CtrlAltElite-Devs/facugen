PROMPT_TEMPLATE = """
Generate ONE short student feedback sentence.

Context:
- University course or instructor feedback

Rules:
- {language_rule}
- Sentiment: {label}
- Length: 5 to 15 words
- Natural and conversational
- No emojis
- No explanations

Return ONLY valid JSON in this exact format:

{{
  "text": "...",
  "label": "{label}",
  "lang_type": "{lang_type}"
}}
""".strip()
