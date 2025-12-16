# File: parser.py

import argparse
import re
import json
import sys
import os
from typing import Dict, Any, Optional, List
from collections import Counter

LOG_PATTERN = re.compile(
    r"^\[(.*?)\] \| (\w+) \| \[(.*?)\] \| (.*?) \| (.*?) \| (\{.*\})$"
)


def parse_line(line: str) -> Optional[Dict[str, Any]]:
    # Stripping Whitespace
    line = line.strip()
    # Regex Matching
    match = LOG_PATTERN.match(line)

    if not match:
        return None  # safety return for malformed lines

    # Unpacking Groups
    timestamp, level, service, req_id, message, metadata_str = match.groups()

    # JSON Parsing
    try:
        metadata = json.loads(metadata_str)
    except json.JSONDecodeError:
        return None  # safety return for malformed JSON

    # Returning Parsed Data with Dictionary type
    return {
        "timestamp": timestamp,
        "level": level,
        "service": service,
        "request_id": req_id,
        "message": message,
        "metadata": metadata,
    }


def parserArguments(args=None):
    parser = argparse.ArgumentParser(
        description="Process log files and extract error information."
    )

    # ful_path = os.path.abspath(__file__)
    parser.add_argument(
        "-i",
        "--input",  # add - i replace for --input || Ver1.1
        required=True,
        help=f"Path to the input log file.",
    )
    parser.add_argument(
        "-o",
        "--output",  # add - o replace for --output || Ver1.1
        required=True,
        help="Path to the output report file.",
    )
    parser.add_argument(
        "-v",
        "--verbose",  # add - v replace for --verbose || Ver1.1
        action="store_true",
        help="Enable all output information.",
    )
    return parser.parse_args(args)


def processLogFile(input, verbose=False) -> Optional[Dict[str, Any]]:
    total_lines = 0
    malformed_lines = 0
    errors_list: List[Dict[str, Any]] = []

    try:
        with open(input, "r", encoding="utf-8") as f:
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
            print(f"Processing {input}...")
            print(
                "---------------------------------------------------------------------------------"
            )
            print(f"\nTotal Lines Processed: {total_lines}")
            print(f"Malformed Lines Skipped: {malformed_lines}")

    except FileNotFoundError:
        print(f"Error: File '{input}' not found.")
        sys.exit(1)

    return errors_list


def processError(errors_list: List[Dict[str, Any]], output, verbose=False) -> None:
    total_errors = len(errors_list)
    error_messages = [e["message"] for e in errors_list]
    error_counts = Counter(error_messages)

    affected_users = [e["user_id"] for e in errors_list if e["user_id"] is not None]
    user_counts = Counter(affected_users)
    unique_users_count = len(user_counts)

    if verbose:
        print(
            "---------------------------------------------------------------------------------"
        )
        print(f"\nTotal Errors Found: {total_errors}")

        print("\nTop Error Messages:")
        for msg, count in error_counts.most_common():
            print(f" - {msg} ({count} occurrences)")

        print("\nAffected Users:")
        for user, count in user_counts.items():
            print(f" - User ID: {user} ({count} errors)")

        print(
            "---------------------------------------------------------------------------------"
        )
        print(f"\nReport saved to {output}")

    report_data = {
        "summary": {
            "total_errors": total_errors,
            "unique_affected_users": unique_users_count,
        },
        "errors": errors_list,
    }

    with open(output, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    return errors_list


def main():
    # Parsing Command Line Arguments
    args = parserArguments()

    # Processing Log File
    errorCollection = processLogFile(args.input, args.verbose)

    # Collecting Errors and Generating Report
    processError(errorCollection, args.output, args.verbose)


if __name__ == "__main__":
    main()
