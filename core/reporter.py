from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from core.theme import console


def print_analysis_report(
    components,
    keywords,
    score,
    level,
    verification
):
    # -----------------------------
    # URL INFORMATION
    # -----------------------------
    url_table = Table(title="URL Information")

    url_table.add_column("Field", style="cyan", no_wrap=True)
    url_table.add_column("Value", style="white")

    url_table.add_row("Original URL", components["original_url"])
    url_table.add_row("Protocol", components["protocol"])
    url_table.add_row("Domain", components["domain"])
    url_table.add_row("Path", components["path"] or "-")
    url_table.add_row("Query", components["query"] or "-")
    url_table.add_row("Fragment", components["fragment"] or "-")

    console.print(url_table)

    # -----------------------------
    # OFFICIAL DOMAIN VERIFICATION
    # -----------------------------
    verification_table = Table(title="Official Domain Verification")

    verification_table.add_column("Property", style="cyan")
    verification_table.add_column("Value", style="white")

    verification_table.add_row(
        "Status",
        "✔ Verified" if verification["verified"] else "✖ Not Verified"
    )

    verification_table.add_row(
        "Bank",
        verification["bank"] or "-"
    )

    verification_table.add_row(
        "Official Domain",
        verification["official_domain"] or "-"
    )

    verification_table.add_row(
        "Closest Domain",
        verification["closest_domain"] or "-"
    )

    verification_table.add_row(
        "Similarity",
        f'{verification["similarity"]}%'
    )

    verification_table.add_row(
        "Possible Typosquatting",
        "Yes" if verification["possible_typosquatting"] else "No"
    )

    console.print(verification_table)

    # -----------------------------
    # KEYWORD ANALYSIS
    # -----------------------------
    keyword_table = Table(title="Detected Keywords")

    keyword_table.add_column("Keyword", style="yellow")

    if keywords:

        for keyword in keywords:

            keyword_table.add_row(keyword)

    else:

        keyword_table.add_row(
            "No suspicious phishing keywords detected."
        )

    console.print(keyword_table)

    # -----------------------------
    # RISK SCORE
    # -----------------------------
    if level == "LOW":

        color = "green"

    elif level == "MEDIUM":

        color = "yellow"

    else:

        color = "red"

    console.print(
        Panel.fit(
            f"[bold]{score}/100[/bold]\n"
            f"Risk Level: [{color}]{level}[/{color}]",
            title="Security Assessment",
            border_style=color
        )
    )

    # -----------------------------
    # RECOMMENDATIONS
    # -----------------------------
    recommendations = Text()

    recommendations.append(
        "Recommendations\n\n",
        style="bold cyan"
    )

    if verification["verified"]:

        recommendations.append(
            "✔ This website matches an official bank domain.\n"
        )

    else:

        recommendations.append(
            "• Verify the official bank domain.\n"
        )

        if verification["possible_typosquatting"]:

            recommendations.append(
                "• This website may be impersonating an official bank.\n"
            )

    recommendations.append(
        "• Never share OTP or SMS verification codes.\n"
    )

    recommendations.append(
        "• Check the SSL certificate before logging in.\n"
    )

    recommendations.append(
        "• Contact your bank through official channels if unsure.\n"
    )

    console.print(
        Panel(
            recommendations,
            title="Security Recommendations",
            border_style="blue"
        )
    )