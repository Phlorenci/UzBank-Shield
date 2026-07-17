from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from core.theme import console


def print_analysis_report(components, keywords, score, level):

    table = Table(title="URL INFORMATION")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Original URL", components["original_url"])
    table.add_row("Protocol", components["protocol"])
    table.add_row("Domain", components["domain"])
    table.add_row("Path", components["path"] or "-")
    table.add_row("Query", components["query"] or "-")
    table.add_row("Fragment", components["fragment"] or "-")

    console.print(table)

    keyword_table = Table(title="Detected Keywords")

    keyword_table.add_column("Keyword")

    if keywords:

        for keyword in keywords:

            keyword_table.add_row(keyword)

    else:

        keyword_table.add_row("None")

    console.print(keyword_table)

    if level == "LOW":

        color = "green"

    elif level == "MEDIUM":

        color = "yellow"

    else:

        color = "red"

    console.print(
        Panel.fit(
            f"[bold]{score}/100[/bold]\nRisk Level: [{color}]{level}[/{color}]",
            title="Security Assessment",
            border_style=color
        )
    )

    recommendations = Text()

    recommendations.append("Recommendations\n\n", style="bold cyan")

    recommendations.append("• Verify the official domain\n")
    recommendations.append("• Never share OTP codes\n")
    recommendations.append("• Check SSL certificate\n")
    recommendations.append("• Compare the URL carefully\n")
    recommendations.append("• Contact the bank if unsure")

    console.print(
        Panel(
            recommendations,
            border_style="blue"
        )
    )