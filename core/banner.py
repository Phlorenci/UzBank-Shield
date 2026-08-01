# Welcome banner
from rich.console import Console
from rich.rule import Rule

from core.__version__ import __version__
from core.messages import get_message

console = Console()


def print_banner(language="en"):
    console.print()
    console.print(Rule("[bold cyan]UzBank Shield[/bold cyan]"))
    console.print(get_message("banner_subtitle", language))
    console.print(f"Version {__version__}")
    console.print(Rule(style="cyan"))
    console.print(f"[green]Status:[/green] {get_message('banner_status_ready', language)}\n")
    