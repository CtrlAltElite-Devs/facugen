from facugen.prompts.language_rules import LANGUAGE_RULES
from facugen.prompts.templates import PROMPT_TEMPLATE


def build_prompt(lang_type: str, label: str) -> str:
    try:
        language_rule = LANGUAGE_RULES[lang_type]
    except KeyError:
        raise ValueError(f"Unsupported language type: {lang_type}")

    return PROMPT_TEMPLATE.format(
        language_rule=language_rule, label=label, lang_type=lang_type
    )
