def is_valid_sample(sample: dict, *, label: str, lang_type: str) -> bool:
    if not isinstance(sample, dict):
        return False

    if sample.get("label") != label:
        return False

    if sample.get("lang_type") != lang_type:
        return False

    text = sample.get("text")
    if not isinstance(text, str):
        return False

    word_count = len(text.split())
    if word_count < 5 or word_count > 15:
        return False

    return True
