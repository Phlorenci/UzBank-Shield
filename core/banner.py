# Welcome banner
from rich.panel import Panel
from rich.align import Align
from core.theme import console


def print_banner():

    banner = """
████████╗██████╗
╚══██╔══╝██╔══██╗
   ██║   ██████╔╝
   ██║   ██╔══██╗
   ██║   ██████╔╝
   ╚═╝   ╚═════╝

      UZBANK SHIELD
"""

    console.print()

    console.print(
        Panel.fit(
            Align.center(banner),
            title="Cybersecurity Toolkit",
            subtitle="Version 0.3.0",
            border_style="cyan"
        )
    )

    console.print("[green]Protect • Detect • Verify[/green]")