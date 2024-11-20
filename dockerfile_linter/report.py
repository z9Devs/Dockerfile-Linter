from rich.console import Console
from rich.table import Table

def generate_report(issues):
    """Generates a readable report in the terminal."""
    console = Console()
    table = Table(title="Dockerfile Analysis Report")
    table.add_column("Check", justify="left", style="bold")
    table.add_column("Status", justify="left", style="red")

    if issues:
        for issue in issues:
            table.add_row(issue, "FAIL")
    else:
        table.add_row("All checks passed", "OK")
    
    console.print(table)