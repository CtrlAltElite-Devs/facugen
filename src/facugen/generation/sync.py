from tqdm import tqdm
from facugen.generation.planner import plan_labels
import json
import random
import time

from facugen.prompts.builder import build_prompt
from facugen.core import is_valid_sample, Label
from facugen.providers import LLMProvider


LABELS: list[Label] = ["positive", "neutral", "negative"]


def generate_one(
    provider: LLMProvider,
    *,
    lang_type: str,
    label: str,
    max_retries: int = 5,
):
    prompt = build_prompt(lang_type, label)

    last_error = None

    for attempt in range(max_retries):
        try:
            raw = provider.generate(prompt)
            sample = json.loads(raw)

            if is_valid_sample(sample, label=label, lang_type=lang_type):
                return sample

            last_error = "Schema validation failed"

        except Exception as e:
            last_error = str(e)
            if "RESOURCE_EXHAUSTED" in last_error or "429" in last_error:
                # Exponential backoff: 2, 4, 8, 16... + jitter
                sleep_time = (2**attempt) + random.random()
                time.sleep(sleep_time)
                continue

    raise RuntimeError(
        f"Failed to generate valid sample after {max_retries} attempts. "
        f"Last error: {last_error}"
    )


def generate_batch(
    provider: LLMProvider,
    *,
    lang_type: str,
    count: int,
    balance_labels: bool = False,
):
    samples = []
    labels = plan_labels(count, balance_labels)

    for label in tqdm(labels, desc="Generating samples", unit="sample"):
        sample = generate_one(
            provider,
            lang_type=lang_type,
            label=label,
        )
        samples.append(sample)

    return samples
