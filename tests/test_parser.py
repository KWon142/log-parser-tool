import pytest
import json
import os
import sys

# Add parent directory to sys.path to allow importing parser.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser import parse_line, processLogFile, processError

# --- FIXTURES (Reusable Sample Data) ---


@pytest.fixture
def sample_log_line_valid():
    """Returns a valid INFO log line sample."""
    return '[2025-12-16 10:00:00] | INFO | [AuthService] | req-123 | User logged in | {"user_id": 101, "ip": "192.168.1.1"}'


@pytest.fixture
def sample_log_line_error():
    """Returns a valid ERROR log line sample."""
    return '[2025-12-16 10:05:00] | ERROR | [PaymentService] | req-456 | Payment failed | {"user_id": 102, "error_code": 500}'


@pytest.fixture
def sample_log_line_malformed():
    """Returns a malformed log line (incorrect regex structure)."""
    return "Invalid log line content here"


@pytest.fixture
def sample_log_line_bad_json():
    """Returns a log line with valid structure but invalid JSON metadata."""
    return "[2025-12-16 10:00:00] | INFO | [Service] | req-1 | Msg | {invalid_json}"


# --- UNIT TESTS ---


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


def test_process_log_file(tmp_path, sample_log_line_valid, sample_log_line_error):
    """
    Test reading and filtering logs from a file.
    Uses 'tmp_path' fixture to create temporary files isolated from the OS.
    """
    # 1. Create a dummy log file in the temp directory
    d = tmp_path / "logs"
    d.mkdir()
    p = d / "test.log"

    # Write mixed content: 1 Valid INFO, 1 Valid ERROR, 1 Malformed
    content = f"{sample_log_line_valid}\n{sample_log_line_error}\nInvalid Line"
    p.write_text(content, encoding="utf-8")

    # 2. Call the function under test
    errors = processLogFile(str(p), verbose=False)

    # 3. Assertions
    # Only the ERROR line should be captured
    assert len(errors) == 1
    assert errors[0]["service"] == "PaymentService"
    assert errors[0]["user_id"] == 102


def test_process_log_file_not_found():
    """Test behavior when the input file does not exist (expecting SystemExit)."""
    with pytest.raises(SystemExit):
        processLogFile("non_existent_file.log")


def test_process_error_report(tmp_path):
    """Test generating the JSON report from a list of errors."""
    # 1. Prepare input data
    errors_list = [
        {"timestamp": "t1", "service": "S1", "message": "Error A", "user_id": 1},
        {
            "timestamp": "t2",
            "service": "S1",
            "message": "Error A",
            "user_id": 1,
        },  # Duplicate error/user
        {"timestamp": "t3", "service": "S2", "message": "Error B", "user_id": 2},
    ]

    # 2. Define output path in temp directory
    output_file = tmp_path / "report.json"

    # 3. Call the function
    processError(errors_list, str(output_file), verbose=False)

    # 4. Verify file creation
    assert output_file.exists()

    # 5. Read back the JSON to verify logic (counting and structure)
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Check statistics logic
    assert data["summary"]["total_errors"] == 3
    assert data["summary"]["unique_affected_users"] == 2  # User 1 and User 2
    assert len(data["errors"]) == 3
