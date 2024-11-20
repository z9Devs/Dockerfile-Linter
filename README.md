
# Dockerfile Linter

**Dockerfile Linter** is an open-source tool written in Python that analyzes your Dockerfiles and provides a report with suggestions based on best practices. It helps optimize and secure your containers.

## Features

- Base image analysis (e.g., avoiding the use of `latest` or recommending lighter images).
- Verification of non-root user usage.
- Suggestions for combining `RUN` commands to reduce layers.
- Support for Dockerfiles with custom names.

---

## Requirements

- Python 3.9 or higher
- Python libraries:
  - `dockerfile-parse`
  - `pytest`
  - `rich`

You can install the requirements with:
```bash
pip install -r requirements.txt
```

---

## Installation

Clone the repository and set up the virtual environment:
```bash
git clone https://github.com/la-plas-growth/Dockerfile-Linter.git
cd dockerfile-linter
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

### Analyze a Dockerfile
To analyze a Dockerfile, run:
```bash
python main.py /path/to/Dockerfile
```

### Specify a Custom Name for the Dockerfile
The linter supports files with custom names:
```bash
python main.py /path/to/custom_dockerfile
```

### Options
- You can choose the output format (text or JSON):
  ```bash
  python main.py /path/to/Dockerfile --output json
  ```
- Ignore specific checks:
  ```bash
  python main.py /path/to/Dockerfile --ignore "Base Image Check"
  ```

---

## Output Example

**Text Output**:
```
+----------------------------+----------+-----------------------------------------------+
| Check                      | Severity | Suggestion                                    |
+----------------------------+----------+-----------------------------------------------+
| Avoid using 'latest' tag   | WARN     | Specify a version like 'python:3.9-slim'.    |
| No non-root user specified | FAIL     | Consider adding a non-root USER instruction. |
+----------------------------+----------+-----------------------------------------------+
```

**JSON Output**:
```json
{
  "issues": [
    {
      "check": "Avoid using 'latest' tag for base images.",
      "severity": "WARN",
      "suggestion": "Specify a version like 'python:3.9-slim'."
    },
    {
      "check": "No non-root user specified.",
      "severity": "FAIL",
      "suggestion": "Consider adding a non-root USER instruction."
    }
  ]
}
```

---

## Tests

Run tests to ensure the project is working correctly:
```bash
pytest
```

The `pytest` framework will automatically test the project's main functions.

---

## Project Structure

```
dockerfile-linter/
├── dockerfile_linter/
│   ├── __init__.py       # Main module file
│   ├── checks.py         # Best practice checks
│   ├── core.py           # Dockerfile parsing
│   ├── report.py         # Report generation
├── tests/
│   └── test_core.py      # Tests for core functionalities
├── main.py               # Program entry point
├── Dockerfile            # Example Dockerfile
├── Dockerfile.bad        # Dockerfile with errors for testing
├── README.md             # Documentation
```

---

## Contributions

If you have ideas to improve the project or have found a bug, open an issue or submit a pull request on GitHub.

---

## License

This project is distributed under the MIT license. See the `LICENSE` file for details.

---

### Contact Us

For questions or suggestions, email: **info@laplasgrowth.it**.
