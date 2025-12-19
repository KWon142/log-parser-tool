# File: parser.py

import argparse
import json
import re
import sys
from collections import Counter
from typing import Any, Dict, List, Optional

# Constants should be UPPER_CASE
LOG_PATTERN = re.compile(
    r"^\[(.*?)\] \| (\w+) \| \[(.*?)\] \| (.*?) \| (.*?) \| (\{.*\})$"
)


def parse_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse a single line of log into a dictionary."""
    line = line.strip()
    match = LOG_PATTERN.match(line)

    if not match:
        return None

    timestamp, level, service, req_id, message, metadata_str = match.groups()

    try:
        metadata = json.loads(metadata_str)
    except json.JSONDecodeError:
        return None

    return {
        "timestamp": timestamp,
        "level": level,
        "service": service,
        "request_id": req_id,
        "message": message,
        "metadata": metadata,
    }


def parse_arguments(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process log files and extract error information."
    )

    parser.add_argument(
        "-i",
        "--input",
        dest="input_path",  # Map --input to variable 'input_path'
        required=True,
        help="Path to the input log file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        required=True,
        help="Path to the output report file.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable all output information.",
    )

    # Allow passing args list for easier testing
    return parser.parse_args(args)


def process_log_file(input_path: str, verbose: bool = False) -> List[Dict[str, Any]]:
    """Read log file and filter ERROR logs."""
    total_lines = 0
    malformed_lines = 0
    errors_list: List[Dict[str, Any]] = []

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                total_lines += 1
                parsed_data = parse_line(line)

                if parsed_data is None:
                    malformed_lines += 1
                    continue

                if parsed_data["level"] == "ERROR":
                    user_id = parsed_data["metadata"].get("user_id")

                    error_record = {
                        "timestamp": parsed_data["timestamp"],
                        "service": parsed_data["service"],
                        "message": parsed_data["message"],
                        "user_id": user_id,
                    }
                    errors_list.append(error_record)

        if verbose:
            print(f"Processing {input_path}...")
            print("-" * 80)
            print(f"\nTotal Lines Processed: {total_lines}")
            print(f"Malformed Lines Skipped: {malformed_lines}")

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)

    return errors_list


def process_errors(
    errors_list: List[Dict[str, Any]], output_path: str, verbose: bool = False
) -> List[Dict[str, Any]]:
    """Analyze errors and write report to JSON."""
    total_errors = len(errors_list)
    error_messages = [e["message"] for e in errors_list]
    error_counts = Counter(error_messages)

    affected_users = [e["user_id"] for e in errors_list if e["user_id"] is not None]
    user_counts = Counter(affected_users)
    unique_users_count = len(user_counts)

    if verbose:
        print("-" * 80)
        print(f"\nTotal Errors Found: {total_errors}")

        print("\nTop Error Messages:")
        for msg, count in error_counts.most_common():
            print(f" - {msg} ({count} occurrences)")

        print("\nAffected Users:")
        for user, count in user_counts.items():
            print(f" - User ID: {user} ({count} errors)")

        print("-" * 80)
        print(f"\nReport saved to {output_path}")

    report_data = {
        "summary": {
            "total_errors": total_errors,
            "unique_affected_users": unique_users_count,
        },
        "errors": errors_list,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    return errors_list


def main():
    # 1. Parsing Arguments
    args = parse_arguments()

    # 2. Processing Log File
    error_collection = process_log_file(args.input_path, args.verbose)

    # 3. Generating Report
    process_errors(error_collection, args.output_path, args.verbose)


if __name__ == "__main__":
    main()
