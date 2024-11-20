def check_base_image(base_image):
    """Checks if the base image is specific and optimized."""
    issues = []
    if ":latest" in base_image:
        issues.append((
            "Avoid using 'latest' tag for base images.",
            "WARN",
            "Specify a version like 'python:3.9-slim'."
        ))
    if not any(tag in base_image for tag in ["slim", "alpine"]):
        issues.append((
            f"Consider using a smaller base image instead of {base_image}.",
            "INFO",
            "Use 'python:3.9-slim' or 'python:3.9-alpine'."
        ))
    return issues

def check_non_root_user(instructions):
    """Checks if a non-root USER instruction is present."""
    for instr in instructions:
        if instr['instruction'] == 'USER' and instr['value'] != 'root':
            return []  # No issues found
    return [(
        "No non-root user specified.",
        "FAIL",
        "Consider adding a non-root USER instruction."
    )]

def check_optimized_run(instructions):
    """Checks if RUN commands are optimized."""
    for instr in instructions:
        if instr['instruction'] == 'RUN' and '&&' not in instr['value']:
            return [(
                "Combine RUN commands to reduce image layers.",
                "WARN",
                "Use '&&' to chain commands in a single RUN."
            )]
    return []  # No issues found
