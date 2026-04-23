from __future__ import annotations

import argparse

from .config import load_topic_config
from .pipeline import ResearchPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="paperclip-kratos", description="Research automation MVP"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Run research pipeline")
    run_parser.add_argument("--config", required=True, help="Path to topic config JSON")
    run_parser.add_argument(
        "--output-dir", default="output", help="Directory for generated files"
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        config = load_topic_config(args.config)
        pipeline = ResearchPipeline()
        result = pipeline.run(config=config, output_dir=args.output_dir)
        print(
            f"Run completed: {len(result.sources)} sources generated for topic '{result.topic}'."
        )
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
