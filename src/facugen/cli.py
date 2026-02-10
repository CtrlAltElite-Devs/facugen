import argparse
import asyncio
import json
import sys

from dotenv import load_dotenv

from facugen.async_generator import generate_batch_async
from facugen.constants import SUPPORTED_LANGS
from facugen.generator import generate_batch
from facugen.model_resolver import resolve_model
from facugen.models import SUPPORTED_MODELS
from facugen.provider_factory import create_provider


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="facugen",
        description="Dataset generator CLI for multilingual student feedback",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate training samples")

    generate.add_argument(
        "--lang",
        required=True,
        choices=sorted(SUPPORTED_LANGS),
        help="Language type to generate",
    )

    generate.add_argument(
        "--count", required=True, type=int, help="Number of samples to generate"
    )

    generate.add_argument(
        "--model",
        default="gpt-4o",
        choices=sorted(SUPPORTED_MODELS.keys()),
        help="Model to use for generation (default: %(default)s)",
    )

    generate.add_argument(
        "--out", default="dataset.jsonl", help="Output file path (JSONL format)"
    )

    generate.add_argument(
        "--balance-labels",
        action="store_true",
        help="Generate an equal number of positive, neutral, and negative samples",
    )

    generate.add_argument(
        "--seed", type=int, help="Seed for reproducible dataset generation"
    )

    generate.add_argument(
        "--async",
        action="store_true",
        dest="use_async",
        help="Generate samples concurrently",
    )

    generate.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Max concurrent API requests (async only)",
    )

    return parser


def main(argv=None):
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.seed is not None:
        import random

        random.seed(args.seed)

    try:
        model_spec = resolve_model(args.model)
        provider = create_provider(model_spec)

        if args.use_async:
            samples = asyncio.run(
                generate_batch_async(
                    provider,
                    lang_type=args.lang,
                    count=args.count,
                    balance_labels=args.balance_labels,
                    concurrency=args.concurrency,
                )
            )
        else:
            samples = generate_batch(
                provider,
                lang_type=args.lang,
                count=args.count,
                balance_labels=args.balance_labels,
            )

        # Write JSONL
        from pathlib import Path

        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            for sample in samples:
                f.write(f"{json.dumps(sample, ensure_ascii=False)}\n")

        print(f"Generated {len(samples)} samples -> {args.out}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # TEMP: Just echo parsed arguemnts
    print("Command:", args.command)
    print("Language", args.lang)
    print("Count: ", args.count)
    print("Provider:", model_spec.provider)
    print("Model: ", model_spec.model)


if __name__ == "__main__":
    main()
