import asyncio
from tqdm import tqdm
from facugen.generator import generate_one
from facugen.label_planner import plan_labels
from facugen.providers import LLMProvider


async def generate_one_async(
    semaphore: asyncio.Semaphore,
    provider: LLMProvider,
    *,
    lang_type: str,
    label: str,
):
    async with semaphore:
        # Run the blocking function in a worker thread
        return await asyncio.to_thread(
            generate_one, provider, lang_type=lang_type, label=label
        )


async def generate_batch_async(
    provider: LLMProvider,
    *,
    lang_type: str,
    count: int,
    balance_labels: bool,
    concurrency: int,
):
    labels = plan_labels(count, balance_labels)
    semaphore = asyncio.Semaphore(concurrency)

    tasks = [
        generate_one_async(
            semaphore,
            provider,
            lang_type=lang_type,
            label=label,
        )
        for label in labels
    ]

    results = []
    for f in tqdm(
        asyncio.as_completed(tasks),
        total=len(tasks),
        desc="Generating samples (async)",
        unit="sample",
    ):
        result = await f
        results.append(result)

    return results
