from rich.console import Console
from rich.table import Table

def generate_report(issues):
    """Genera un report leggibile nel terminale."""
    console = Console()
    table = Table(title="Dockerfile Analysis Report")
    table.add_column("Check", justify="left", style="bold")
    table.add_column("Severity", justify="left", style="yellow")
    table.add_column("Suggestion", justify="left", style="green")

    if issues:
        for issue in issues:
            check, severity, suggestion = issue
            table.add_row(check, severity, suggestion)
    else:
        table.add_row("All checks passed", "OK", "Well done!")

    console.print(table)