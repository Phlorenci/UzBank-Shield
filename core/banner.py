# Welcome banner
from rich.console import Console
from rich.rule import Rule

console = Console()


def print_banner():
    console.print()
    console.print(Rule("[bold cyan]UzBank Shield[/bold cyan]"))
    console.print("Cybersecurity URL Analysis Toolkit")
    console.print("Version 0.5.0")
    console.print(Rule(style="cyan"))
    console.print("[green]Status:[/green] Ready\n")