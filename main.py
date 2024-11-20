import argparse
from dockerfile_linter import (
    parse_dockerfile,
    check_base_image,
    check_non_root_user,
    check_optimized_run,
    generate_report
)

def parse_args():
    """Handles CLI arguments."""
    parser = argparse.ArgumentParser(description="Dockerfile Linter")
    parser.add_argument("dockerfile", help="Path to the Dockerfile to analyze")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--ignore", nargs="+", help="List of checks to ignore (e.g., 'Base Image Check')")
    return parser.parse_args()

def main():
    """Main function of the program."""
    args = parse_args()
    
    try:
        # Parse the Dockerfile
        result = parse_dockerfile(args.dockerfile)

        # List of checks to perform
        all_checks = [
            ("Base Image Check", check_base_image(result["base_image"])),
            ("Non-Root User Check", check_non_root_user(result["instructions"])),
            ("Optimized RUN Check", check_optimized_run(result["instructions"]))
        ]
        
        # Filter out ignored checks
        issues = []
        for name, check in all_checks:
            if args.ignore and name in args.ignore:
                continue
            issues.extend(check)
        
        # Generate the report
        if args.output == "text":
            generate_report(issues)
        elif args.output == "json":
            import json
            print(json.dumps({"issues": issues}, indent=2))

    except FileNotFoundError:
        print(f"Error: Dockerfile not found at '{args.dockerfile}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()