import random
from facugen.schema import Label

LABELS: list[Label] = ["positive", "neutral", "negative"]


def plan_labels(count: int, balanced: bool) -> list[Label]:
    if not balanced:
        return [random.choice(LABELS) for _ in range(count)]

    if count % 3 != 0:
        raise ValueError("When using --balance-labels, count must be divisible by 3.")

    per_label = count // 3
    labels: list[Label] = (
        (["positive"] * per_label)
        + (["neutral"] * per_label)
        + (["negative"] * per_label)
    )  # type: ignore

    random.shuffle(labels)

    return labels
