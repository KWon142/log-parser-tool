# Log Parser Tool 🛠️

  


## 📖 Index
- [Log Parser Tool 🛠️](#log-parser-tool-️)
  - [📖 Index](#-index)
  - [🚀 Description](#-description)
  - [✨ Features](#-features)
  - [⚙️ Installation](#️-installation)
    - [Requirements](#requirements)
    - [Installation steps](#installation-steps)
  - [💻 Usage](#-usage)
    - [Command Syntax](#command-syntax)
  - [🗺️ Roadmap](#️-roadmap)
    - [Here are the planned features for future releases:](#here-are-the-planned-features-for-future-releases)
  - [🚧 Project Status](#-project-status)
  - [💬 Support](#-support)
    - [If you encounter any issues or have questions:](#if-you-encounter-any-issues-or-have-questions)


![Python Version](https://img.shields.io/badge/python-3.12+-blue)

## 🚀 Description
The **Log Parser Tool** is designed to solve the problem of reading and understanding large system log files (server logs).
- Read the raw text log file.
- Filter out lines and Analyze `ERROR` messages
- Parse the JSON data in the metadata.
- Provide statistical reports in JSON format (number of errors, affected users).


## ✨ Features
* **High Performance:** Uses Lazy Loading (Stream processing) to handle large log files without consuming excessive RAM.
* **Robust Parsing:** Automatically skips malformed log lines without crashing the program.
* **Statistics:** Displays top frequently encountered errors and a list of affected User IDs.
* **Flexible Output:** Supports exporting reports to standard JSON files.
* **Verbose Mode:** Displays detailed process progress in the Terminal.


## ⚙️ Installation

### Requirements 
* Ubuntu/Linux (recommended) or Windows/macOS.
* Python 3.12 trở lên.
* [uv](https://github.com/astral-sh/uv) (Modern Python package manager).

### Installation steps
1.  **Installing `uv`:**
    * macOS and Linux:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ``` 
    * Windows: 
    ```bash
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    * However, pip can also be used:
    ```bash
    pip install uv
    ```

2.  **Clone the repository to your local machine**
    ```bash
    git clone git@github.com:KWon142/log-parser-tool.git
    cd log-parser-tool
    ```

3.  **Environmental synchronization (Most important)**
    ```bash
    uv sync
    ```

4.  Test run successful** 
    Run the help command to ensure everything is ready.
    ```bashTest
    uv run parser.py --help
    ```
    If the user guide appears -> Setup successful!

## 💻 Usage

### Command Syntax
```bash
uv run parser.py -i <INPUT_FILE> -o <OUTPUT_FILE> [OPTIONS]
```

## 🗺️ Roadmap
### Here are the planned features for future releases:

- [x] Core: Lazy Loading mechanism for large files.

- [x] Reporting: JSON Output format.

- [ ] Feature: Support for CSV and Excel export.

- [ ] Feature: Date range filtering arguments (--start-date, --end-date).

- [ ] Testing: Increase Unit Test coverage to 90%.

- [ ] CI/CD: Automated testing pipeline via GitHub Actions.

## 🚧 Project Status
This project is currently under **active development**.
- **Current Version:** `v1.0.0` (Core Parsing & JSON Reporting).
- **Focus:** We are currently optimizing performance for log files larger than 10GB.

## 💬 Support
    
### If you encounter any issues or have questions:

1. Check the Usage section to ensure correct command syntax.

2. Open an Issue on GitHub with a detailed description and sample log data.

3. Contact the maintainer via email: quan.pham@inexus.ai.
