from datetime import datetime

from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from core.theme import console


def print_analysis_report(
    components,
    keywords,
    score,
    level,
    verification,
    suspicious_tld
):
    # -------------------------------------------------
    # SCAN SUMMARY
    # -------------------------------------------------

    if level == "LOW":
        color = "green"
        recommendation = "Website appears safe."

    elif level == "MEDIUM":
        color = "yellow"
        recommendation = "Proceed with caution."

    else:
        color = "red"
        recommendation = "Do not trust this website."

    summary = Table(title="Scan Summary")

    summary.add_column("Property", style="cyan")
    summary.add_column("Value", style="white")

    summary.add_row(
        "Scan Time",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    summary.add_row(
        "Risk Score",
        f"{score}/100"
    )

    summary.add_row(
        "Risk Level",
        f"[{color}]{level}[/{color}]"
    )

    summary.add_row(
        "Official Bank",
        "Yes" if verification["verified"] else "No"
    )

    summary.add_row(
        "Recommendation",
        recommendation
    )

    console.print(summary)

    # -------------------------------------------------
    # URL INFORMATION
    # -------------------------------------------------

    url_table = Table(title="URL Information")

    url_table.add_column(
        "Field",
        style="cyan",
        no_wrap=True
    )

    url_table.add_column(
        "Value",
        style="white"
    )

    url_table.add_row(
        "Original URL",
        components["original_url"]
    )

    url_table.add_row(
        "Protocol",
        components["protocol"]
    )

    url_table.add_row(
        "Domain",
        components["domain"]
    )

    url_table.add_row(
        "Path",
        components["path"] or "-"
    )

    url_table.add_row(
        "Query",
        components["query"] or "-"
    )

    url_table.add_row(
        "Fragment",
        components["fragment"] or "-"
    )

    console.print(url_table)

    # -------------------------------------------------
    # DOMAIN VERIFICATION
    # -------------------------------------------------

    verification_table = Table(
        title="Official Domain Verification"
    )

    verification_table.add_column(
        "Property",
        style="cyan"
    )

    verification_table.add_column(
        "Value"
    )

    verification_table.add_row(
        "Status",
        "Verified"
        if verification["verified"]
        else "Not Verified"
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
        "Possible Bank Impersonation",
        "Yes"
        if verification["possible_typosquatting"]
        else "No"
    )

    console.print(verification_table)

    # -------------------------------------------------
    # KEYWORD ANALYSIS
    # -------------------------------------------------

    keyword_table = Table(
        title="Detected Keywords"
    )

    keyword_table.add_column(
        "Keyword",
        style="yellow"
    )

    if keywords:

        for keyword in keywords:

            keyword_table.add_row(keyword)

    else:

        keyword_table.add_row("None")

    console.print(keyword_table)

    # -------------------------------------------------
    # RISK ANALYSIS
    # -------------------------------------------------

    analysis = Table(
        title="Risk Analysis"
    )

    analysis.add_column(
        "Security Check",
        style="cyan"
    )

    analysis.add_column(
        "Result"
    )

    analysis.add_row(
        "Official Domain",
        "PASS"
        if verification["verified"]
        else "FAIL"
    )

    analysis.add_row(
        "Possible Impersonation",
        "Detected"
        if verification["possible_typosquatting"]
        else "Not Detected"
    )

    analysis.add_row(
        "Suspicious TLD",
        "Yes"
        if suspicious_tld
        else "No"
    )

    analysis.add_row(
        "Detected Keywords",
        str(len(keywords))
    )

    console.print(analysis)

    # -------------------------------------------------
    # SECURITY SCORE
    # -------------------------------------------------

    console.print(
        Panel.fit(
            f"[bold]{score}/100[/bold]\n"
            f"Risk Level: [{color}]{level}[/{color}]",
            title="Security Score",
            border_style=color
        )
    )

    # -------------------------------------------------
    # RECOMMENDATIONS
    # -------------------------------------------------

    recommendations = Text()

    recommendations.append(
        "Recommendations\n\n",
        style="bold cyan"
    )

    if verification["verified"]:

        recommendations.append(
            "• This domain matches an official bank.\n"
        )

    else:

        recommendations.append(
            "• Verify the domain before entering personal information.\n"
        )

    if verification["possible_typosquatting"]:

        recommendations.append(
            "• This website appears to imitate an official bank.\n"
        )

    if suspicious_tld:

        recommendations.append(
            "• This website uses a suspicious domain extension.\n"
        )

    recommendations.append(
        "• Never share OTP or SMS verification codes.\n"
    )

    recommendations.append(
        "• Check the SSL certificate.\n"
    )

    recommendations.append(
        "• Contact the bank if you are unsure.\n"
    )

    console.print(
        Panel(
            recommendations,
            title="Security Recommendations",
            border_style="blue"
        )
    )