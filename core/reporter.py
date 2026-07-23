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
    suspicious_tld,
    connection,
    ssl_info,
    domain_info
):
    # -------------------------------------------------
    # SUMMARY
    # -------------------------------------------------

    if level == "LOW":
        color = "green"
        recommendation = "Low Risk"

    elif level == "MEDIUM":
        color = "yellow"
        recommendation = "Proceed With Caution"

    else:
        color = "red"
        recommendation = "High Risk"

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
        "Recommendation",
        recommendation
    )

    console.print(summary)

    # -------------------------------------------------
    # URL INFORMATION
    # -------------------------------------------------

    url_table = Table(title="URL Information")

    url_table.add_column("Field", style="cyan")
    url_table.add_column("Value")

    url_table.add_row("Original URL", components["original_url"])
    url_table.add_row("Protocol", components["protocol"])
    url_table.add_row("Domain", components["domain"])
    url_table.add_row("Path", components["path"] or "-")
    url_table.add_row("Query", components["query"] or "-")
    url_table.add_row("Fragment", components["fragment"] or "-")

    console.print(url_table)

    # -------------------------------------------------
    # WEBSITE CONNECTION
    # -------------------------------------------------

    connection_table = Table(title="Website Connection")

    connection_table.add_column("Property", style="cyan")
    connection_table.add_column("Value")

    connection_table.add_row(
        "Protocol",
        connection["protocol"]
    )

    connection_table.add_row(
        "Reachable",
        "Yes" if connection["reachable"] else "No"
    )

    connection_table.add_row(
        "HTTP Status",
        str(connection["status_code"] or "-")
    )

    console.print(connection_table)

    # -------------------------------------------------
    # SSL CERTIFICATE
    # -------------------------------------------------

    ssl_table = Table(title="SSL Certificate")

    ssl_table.add_column("Property", style="cyan")
    ssl_table.add_column("Value")

    if ssl_info["valid"] is True:
        status = "[green]Valid[/green]"
    elif ssl_info["valid"] is False:
        status = "[red]Invalid[/red]"
    else:
        status = "[yellow]Unknown[/yellow]"
    
    ssl_table.add_row("Status", status)

    ssl_table.add_row(
        "Issuer",
        ssl_info["issuer"] or "-"
    )

    ssl_table.add_row(
        "Expires",
        ssl_info["expires"] or "-"
    )

    ssl_table.add_row(
        "Days Remaining",
        str(ssl_info["days_remaining"])
        if ssl_info["days_remaining"] is not None
        else "-"
    )

    console.print(ssl_table)

    # -------------------------------------------------
    # DOMAIN INFORMATION
    # -------------------------------------------------

    domain_table = Table(title="Domain Information")

    domain_table.add_column("Property", style="cyan")
    domain_table.add_column("Value")

    domain_table.add_row(
        "WHOIS Data",
        "Available" if domain_info["available"] else "Not Available"
    )

    domain_table.add_row(
        "Registrar",
        domain_info["registrar"] or "-"
    )

    domain_table.add_row(
        "Created",
        domain_info["created"] or "-"
    )

    if domain_info["age_days"] is not None:
        age_display = f'{domain_info["age_days"]} days'
    else:
        age_display = "-"

    domain_table.add_row(
        "Domain Age",
        age_display
    )

    console.print(domain_table)

    # -------------------------------------------------
    # OFFICIAL DOMAIN VERIFICATION
    # -------------------------------------------------

    verification_table = Table(
        title="Official Domain Verification"
    )

    verification_table.add_column("Property", style="cyan")
    verification_table.add_column("Value")

    verification_table.add_row(
        "Status",
        "Verified" if verification["verified"] else "Not Verified"
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
        "Yes" if verification["possible_typosquatting"] else "No"
    )

    console.print(verification_table)

    # -------------------------------------------------
    # DETECTED KEYWORDS
    # -------------------------------------------------

    keyword_table = Table(title="Detected Keywords")

    keyword_table.add_column("Keyword", style="yellow")

    if keywords:

        for keyword in keywords:

            keyword_table.add_row(keyword)

    else:

        keyword_table.add_row("None")

    console.print(keyword_table)

    # -------------------------------------------------
    # RISK ANALYSIS
    # -------------------------------------------------

    analysis = Table(title="Risk Analysis")

    analysis.add_column("Security Check", style="cyan")
    analysis.add_column("Result")

    analysis.add_row(
        "Official Domain",
        "PASS" if verification["verified"] else "FAIL"
    )

    analysis.add_row(
        "HTTPS",
        "PASS" if connection["https"] else "FAIL"
    )

    if ssl_info["valid"] is True:
        ssl_result = "PASS"
    elif ssl_info["valid"] is False:
        ssl_result = "FAIL"
    else:
        ssl_result = "Not Checked"
    
    analysis.add_row("SSL Certificate", ssl_result)

    if domain_info["available"] and domain_info["age_days"] is not None:
        if domain_info["age_days"] < 30:
            age_result = "FAIL"
        elif domain_info["age_days"] < 180:
            age_result = "WARNING"
        else:
            age_result = "PASS"
    else:
        age_result = "Not Checked"

    analysis.add_row("Domain Age", age_result)

    analysis.add_row(
        "Reachable",
        "PASS" if connection["reachable"] else "FAIL"
    )

    analysis.add_row(
        "Possible Impersonation",
        "Detected"
        if verification["possible_typosquatting"]
        else "Not Detected"
    )

    analysis.add_row(
        "Suspicious TLD",
        "Yes" if suspicious_tld else "No"
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

    if not connection["https"]:
        recommendations.append(
            "• This website uses HTTP instead of HTTPS.\n"
        )

    if not connection["reachable"]:
        recommendations.append(
            "• The website could not be reached.\n"
        )

    if verification["verified"]:
        recommendations.append(
            "• The domain matches an official bank.\n"
        )
    else:
        recommendations.append(
            "• Verify the domain before entering personal information.\n"
        )

    if verification["possible_typosquatting"]:
        recommendations.append(
            "• This website may be impersonating an official bank.\n"
        )

    if suspicious_tld:
        recommendations.append(
            "• This website uses a suspicious top-level domain.\n"
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

    if not ssl_info["valid"]:
        recommendations.append(
        "• This website does not have a valid SSL certificate.\n"
        )

    elif (
    ssl_info["days_remaining"] is not None
    and ssl_info["days_remaining"] < 30
    ):
        
        recommendations.append(
        "• The SSL certificate will expire soon.\n"
    )

    if domain_info["available"] and domain_info["age_days"] is not None:

        if domain_info["age_days"] < 30:
            recommendations.append(
                "• This domain was registered very recently, which is common for phishing sites.\n"
            )
        elif domain_info["age_days"] < 180:
            recommendations.append(
                "• This domain is relatively new; proceed with extra caution.\n"
            )

    console.print(
        Panel(
            recommendations,
            title="Security Recommendations",
            border_style="blue"
        )
    )