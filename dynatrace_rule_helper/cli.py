import argparse
import json
import sys
from pathlib import Path

from dynatrace_rule_helper.engine.core import process_log_file

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate Dynatrace PARSE (DPL) rules from a sample log file.")
    parser.add_argument("-f", "--file", required=True,
                        help="Path to a JSON file containing the raw log event (must have a 'content' field).")
    parser.add_argument("-l", "--literal",
                        help="Comma‑separated literal(s) that precede the value(s) to extract. Optional – if omitted, inferred.")
    parser.add_argument("-v", "--value",
                        help="Comma‑separated value(s) to extract (used for literal inference). Optional.")
    parser.add_argument("-t", "--type",
                        help="Comma‑separated matcher type(s) (INT, FLOAT, STRING, ENUM, REGEX, ...). Optional – inferred from value.")
    parser.add_argument("-a", "--alias", required=True,
                        help="Comma‑separated field name(s) for the extracted data (e.g., 'aws.billed.duration').")
    parser.add_argument("--custom", help="Comma‑separated raw DPL fragment(s) to use directly, bypassing automatic matcher creation. Useful for advanced matchers like ENUM, REGEX, MASK, DROP, etc.")


    parser.add_argument("--open-pipeline", action="store_true",
                        help="If set, output an OpenPipeline YAML snippet instead of classic DPL.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the rule but do not write any output files.")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable debug logging.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    try:
        rule = process_log_file(
            file_path=args.file,
            literals=args.literal,
            values=args.value,
            matcher_types=args.type,
            aliases=args.alias,
            open_pipeline=args.open_pipeline,
            custom=args.custom,
        )
        if args.dry_run:
            print(rule)
        else:
            # By default just print – user can redirect to a file if they wish
            print(rule)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
