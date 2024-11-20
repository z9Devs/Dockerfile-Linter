import sys
import os

# Add the main directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules | need to solve the import path
from dockerfile_linter.core import parse_dockerfile
from dockerfile_linter.checks import check_base_image, check_non_root_user, check_optimized_run
from dockerfile_linter.report import generate_report

def test_parse_dockerfile():
    """Tests the Dockerfile parsing."""
    dockerfile_content = """
FROM python:3.9-slim
WORKDIR /app
COPY . .
CMD ["python", "app.py"]
    """
    temp_file = "Dockerfile"
    with open(temp_file, "w") as f:
        f.write(dockerfile_content)
    
    # Parse the Dockerfile
    result = parse_dockerfile(temp_file)  # Use the correct file name without directories
    
    # Verify the result
    assert result["base_image"] == "python:3.9-slim"
    assert len(result["instructions"]) == 4  # FROM, WORKDIR, COPY, CMD
    
    # Cleanup
    os.remove(temp_file)

def test_check_base_image():
    """Tests the base image check."""
    # Case: correct image
    issues = check_base_image("python:3.9-slim")
    assert issues == []

    # Case: image with "latest"
    issues = check_base_image("python:latest")
    assert len(issues) == 1
    assert issues[0][0] == "Avoid using 'latest' tag for base images."
    assert issues[0][1] == "WARN"
    assert issues[0][2] == "Specify a version like 'python:3.9-slim'."

    # Case: non-optimized image
    issues = check_base_image("python:3.9")
    assert len(issues) == 1
    assert issues[0][0] == "Consider using a smaller base image instead of python:3.9."
    assert issues[0][1] == "INFO"
    assert issues[0][2] == "Use 'python:3.9-slim' or 'python:3.9-alpine'."

def test_check_non_root_user():
    """Tests the non-root user check."""
    # Case: non-root user
    instructions = [{"instruction": "USER", "value": "appuser"}]
    issues = check_non_root_user(instructions)
    assert issues == []

    # Case: root user
    instructions = [{"instruction": "USER", "value": "root"}]
    issues = check_non_root_user(instructions)
    assert len(issues) == 1
    assert issues[0][0] == "No non-root user specified."
    assert issues[0][1] == "FAIL"
    assert issues[0][2] == "Consider adding a non-root USER instruction."

    # Case: no user specified
    instructions = []
    issues = check_non_root_user(instructions)
    assert len(issues) == 1
    assert issues[0][0] == "No non-root user specified."
    assert issues[0][1] == "FAIL"
    assert issues[0][2] == "Consider adding a non-root USER instruction."

def test_check_optimized_run():
    """Tests the optimization of RUN commands."""
    # Case: optimized RUN commands
    instructions = [{"instruction": "RUN", "value": "apt-get update && apt-get install -y curl"}]
    issues = check_optimized_run(instructions)
    assert issues == []

    # Case: non-optimized RUN commands
    instructions = [{"instruction": "RUN", "value": "apt-get update"}]
    issues = check_optimized_run(instructions)
    assert len(issues) == 1
    assert issues[0][0] == "Combine RUN commands to reduce image layers."
    assert issues[0][1] == "WARN"
    assert issues[0][2] == "Use '&&' to chain commands in a single RUN."

def test_generate_report():
    """Tests report generation."""
    issues = [
        ("Avoid using 'latest' tag for base images.", "WARN", "Specify a version like 'python:3.9-slim'."),
        ("No non-root user specified.", "FAIL", "Consider adding a non-root USER instruction."),
    ]
    
    # We cannot directly verify the output of `rich`, but we can ensure it does not fail
    try:
        generate_report(issues)
        assert True  # If it reaches here, the test passed
    except Exception as e:
        assert False, f"generate_report raised an exception: {e}"

    # Case: no issues
    try:
        generate_report([])
        assert True  # If it reaches here, the test passed
    except Exception as e:
        assert False, f"generate_report raised an exception: {e}"
