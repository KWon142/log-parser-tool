import json
import pytest

# Đã xóa import sys (F401 fixed)
from parser import parse_line, parse_arguments, process_log_file, process_errors


# --- FIXTURES (Sample Data) ---


@pytest.fixture
def sample_log_line_valid():
    """Returns a valid INFO log line sample."""
    # Ngắt dòng string dài (E501 fixed)
    return (
        "[2025-12-16 10:00:00] | INFO | [AuthService] | req-123 | "
        'User logged in | {"user_id": 101, "ip": "192.168.1.1"}'
    )


@pytest.fixture
def sample_log_line_error():
    """Returns a valid ERROR log line sample."""
    # Ngắt dòng string dài (E501 fixed)
    return (
        "[2025-12-16 10:05:00] | ERROR | [PaymentService] | req-456 | "
        'Payment failed | {"user_id": 102, "error_code": 500}'
    )


@pytest.fixture
def sample_log_line_malformed():
    """Returns a malformed log line (incorrect regex structure)."""
    return "Invalid log line content here"


@pytest.fixture
def sample_log_line_bad_json():
    """Returns a log line with valid structure but invalid JSON metadata."""
    return "[2025-12-16 10:00:00] | INFO | [Service] | req-1 | Msg | {invalid_json}"


# --- TEST: parse_line ---


def test_parse_line_success(sample_log_line_valid):
    """Test parsing a correctly formatted log line."""
    result = parse_line(sample_log_line_valid)

    assert result is not None
    assert result["timestamp"] == "2025-12-16 10:00:00"
    assert result["level"] == "INFO"
    assert result["service"] == "AuthService"
    assert result["metadata"]["user_id"] == 101


def test_parse_line_malformed(sample_log_line_malformed):
    """Test parsing a malformed line; should return None."""
    result = parse_line(sample_log_line_malformed)
    assert result is None


def test_parse_line_bad_json(sample_log_line_bad_json):
    """Test parsing a line with broken JSON; should handle exception and return None."""
    result = parse_line(sample_log_line_bad_json)
    assert result is None


# --- TEST: parse_arguments ---


def test_parse_arguments_valid():
    """Test parsing valid command-line arguments."""
    # Simulate arguments passed from the terminal
    args_list = ["-i", "input.log", "-o", "output.json", "-v"]
    args = parse_arguments(args_list)

    # Verify if argparse maps arguments correctly to variables
    assert args.input_path == "input.log"
    assert args.output_path == "output.json"
    assert args.verbose is True


def test_parse_arguments_missing_required():
    """Test behavior when required arguments are missing (expecting exit)."""
    # Missing input argument (-i)
    args_list = ["-o", "output.json"]

    # argparse invokes sys.exit(2) when arguments are missing
    with pytest.raises(SystemExit):
        parse_arguments(args_list)


# --- TEST: process_log_file ---


def test_process_log_file(tmp_path, sample_log_line_valid, sample_log_line_error):
    """Test file reading logic and ERROR filtering."""
    # 1. Create a dummy log file in the temporary directory
    log_file = tmp_path / "test.log"
    content = f"{sample_log_line_valid}\n{sample_log_line_error}\nInvalid Line"
    log_file.write_text(content, encoding="utf-8")

    # 2. Call the function
    errors = process_log_file(str(log_file), verbose=False)

    # 3. Verify results
    assert len(errors) == 1
    assert errors[0]["service"] == "PaymentService"
    assert errors[0]["user_id"] == 102


def test_process_log_file_not_found():
    """Test behavior when the input file does not exist."""
    with pytest.raises(SystemExit):
        process_log_file("non_existent_file.log")


# --- TEST: process_errors ---


def test_process_errors_report(tmp_path):
    """Test statistics calculation and JSON report generation."""
    # 1. Prepare dummy input data
    errors_list = [
        {"timestamp": "t1", "service": "S1", "message": "Err A", "user_id": 1},
        {"timestamp": "t2", "service": "S1", "message": "Err A", "user_id": 1},
        {"timestamp": "t3", "service": "S2", "message": "Err B", "user_id": 2},
    ]

    # 2. Define temporary output path
    output_file = tmp_path / "report.json"

    # 3. Call the function
    process_errors(errors_list, str(output_file), verbose=False)

    # 4. Verify output file existence
    assert output_file.exists()

    # 5. Read back the JSON to verify logic
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["summary"]["total_errors"] == 3
    assert data["summary"]["unique_affected_users"] == 2
    assert len(data["errors"]) == 3
