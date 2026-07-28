# Welcome banner
from rich.console import Console
from rich.rule import Rule
from core.__version__ import __version__

console = Console()


def print_banner():
    console.print()
    console.print(Rule("[bold cyan]UzBank Shield[/bold cyan]"))
    console.print("Cybersecurity URL Analysis Toolkit")
    console.print("Version 0.7.0")
    console.print(Rule(style="cyan"))
    console.print("[green]Status:[/green] Ready\n")