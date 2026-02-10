import json
from facugen.generator import generate_batch
from facugen.provider_factory import create_provider
import argparse
import sys
from dotenv import load_dotenv


from facugen.constants import SUPPORTED_LANGS
from facugen.model_resolver import resolve_model
from facugen.models import SUPPORTED_MODELS


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

    return parser


def main(argv=None):
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        model_spec = resolve_model(args.model)
        provider = create_provider(model_spec)

        # Generate samples
        samples = generate_batch(provider, lang_type=args.lang, count=args.count)

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
