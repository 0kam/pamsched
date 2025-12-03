"""
Command-line interface for pamsched.
"""
import argparse
import json
import sys
from pathlib import Path

from .parser import loads, dumps


def main():
    """
    Main entry point for the CLI.
    """
    parser = argparse.ArgumentParser(
        description="Validate and inspect PAM recording schedules."
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        help="Path to the JSON schedule file to validate.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show package version.",
    )

    args = parser.parse_args()

    if args.version:
        # In a real package, we might get this from importlib.metadata
        print("pamsched 0.1.0")
        return

    if not args.file:
        parser.print_help()
        return

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        content = args.file.read_text(encoding="utf-8")
        schedule = loads(content)
        
        print(f"✅ Valid schedule: {args.file}")
        print(f"   Version: {schedule.version}")
        print(f"   Type:    {schedule.pattern_type.value}")
        
        # Pretty print the parsed structure
        print("\nParsed Structure:")
        print(json.dumps(dumps(schedule), indent=2))
        
    except Exception as e:
        print(f"❌ Invalid schedule: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
