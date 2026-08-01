from datetime import datetime

from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from core.theme import console
from core.messages import get_message


def print_analysis_report(
    components,
    keywords,
    score,
    level,
    verification,
    payment_verification,
    suspicious_tld,
    connection,
    ssl_info,
    domain_info,
    language="en"
):
    def _(key):
        return get_message(key, language)

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

    summary = Table(title=_("table_scan_summary"))

    summary.add_column(_("label_property"), style="cyan")
    summary.add_column(_("label_value"), style="white")

    summary.add_row(
        _("label_scan_time"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    summary.add_row(
        _("label_risk_score"),
        f"{score}/100"
    )

    summary.add_row(
        _("label_risk_level"),
        f"[{color}]{level}[/{color}]"
    )

    summary.add_row(
        _("label_recommendation"),
        recommendation
    )

    console.print(summary)

    # -------------------------------------------------
    # URL INFORMATION
    # -------------------------------------------------

    url_table = Table(title=_("table_url_info"))

    url_table.add_column(_("label_field"), style="cyan")
    url_table.add_column(_("label_value"))

    url_table.add_row(_("label_original_url"), components["original_url"])
    url_table.add_row(_("label_protocol"), components["protocol"])
    url_table.add_row(_("label_domain"), components["domain"])
    url_table.add_row(_("label_path"), components["path"] or "-")
    url_table.add_row(_("label_query"), components["query"] or "-")
    url_table.add_row(_("label_fragment"), components["fragment"] or "-")

    console.print(url_table)

    # -------------------------------------------------
    # WEBSITE CONNECTION
    # -------------------------------------------------

    connection_table = Table(title=_("table_connection"))

    connection_table.add_column(_("label_property"), style="cyan")
    connection_table.add_column(_("label_value"))

    connection_table.add_row(
        _("label_protocol"),
        connection["protocol"]
    )

    connection_table.add_row(
        _("label_reachable"),
        _("value_yes") if connection["reachable"] else _("value_no")
    )

    connection_table.add_row(
        _("label_http_status"),
        str(connection["status_code"] or "-")
    )

    console.print(connection_table)

    # -------------------------------------------------
    # SSL CERTIFICATE
    # -------------------------------------------------

    ssl_table = Table(title=_("table_ssl"))

    ssl_table.add_column(_("label_property"), style="cyan")
    ssl_table.add_column(_("label_value"))

    if ssl_info["valid"] is True:
        status = f"[green]{_('value_valid')}[/green]"
    elif ssl_info["valid"] is False:
        status = f"[red]{_('value_invalid')}[/red]"
    else:
        status = f"[yellow]{_('unknown')}[/yellow]"

    ssl_table.add_row(_("label_status"), status)

    ssl_table.add_row(
        _("label_issuer"),
        ssl_info["issuer"] or "-"
    )

    ssl_table.add_row(
        _("label_expires"),
        ssl_info["expires"] or "-"
    )

    ssl_table.add_row(
        _("label_days_remaining"),
        str(ssl_info["days_remaining"])
        if ssl_info["days_remaining"] is not None
        else "-"
    )

    console.print(ssl_table)

    # -------------------------------------------------
    # DOMAIN INFORMATION
    # -------------------------------------------------

    domain_table = Table(title=_("table_domain_info"))

    domain_table.add_column(_("label_property"), style="cyan")
    domain_table.add_column(_("label_value"))

    domain_table.add_row(
        _("label_whois_data"),
        _("value_available") if domain_info["available"] else _("value_not_available")
    )

    domain_table.add_row(
        _("label_registrar"),
        domain_info["registrar"] or "-"
    )

    domain_table.add_row(
        _("label_created"),
        domain_info["created"] or "-"
    )

    if domain_info["age_days"] is not None:
        age_display = f'{domain_info["age_days"]} {_("label_days_suffix")}'
    else:
        age_display = "-"

    domain_table.add_row(
        _("label_domain_age"),
        age_display
    )

    console.print(domain_table)

    # -------------------------------------------------
    # OFFICIAL DOMAIN VERIFICATION
    # -------------------------------------------------

    verification_table = Table(
        title=_("table_bank_verification")
    )

    verification_table.add_column(_("label_property"), style="cyan")
    verification_table.add_column(_("label_value"))

    verification_table.add_row(
        _("label_status"),
        _("verified") if verification["verified"] else _("not_verified")
    )

    verification_table.add_row(
        _("label_bank"),
        verification["bank"] or "-"
    )

    verification_table.add_row(
        _("label_official_domain"),
        verification["official_domain"] or "-"
    )

    verification_table.add_row(
        _("label_closest_domain"),
        verification["closest_domain"] or "-"
    )

    verification_table.add_row(
        _("label_similarity"),
        f'{verification["similarity"]}%'
    )

    verification_table.add_row(
        _("label_possible_impersonation"),
        _("value_yes") if verification["possible_typosquatting"] else _("value_no")
    )

    console.print(verification_table)

    # -------------------------------------------------
    # OFFICIAL PAYMENT PROCESSOR VERIFICATION
    # -------------------------------------------------

    payment_table = Table(
        title=_("table_payment_verification")
    )

    payment_table.add_column(_("label_property"), style="cyan")
    payment_table.add_column(_("label_value"))

    payment_table.add_row(
        _("label_status"),
        _("verified") if payment_verification["verified"] else _("not_verified")
    )

    payment_table.add_row(
        _("label_processor"),
        payment_verification["processor"] or "-"
    )

    payment_table.add_row(
        _("label_official_domain"),
        payment_verification["official_domain"] or "-"
    )

    payment_table.add_row(
        _("label_closest_domain"),
        payment_verification["closest_domain"] or "-"
    )

    payment_table.add_row(
        _("label_similarity"),
        f'{payment_verification["similarity"]}%'
    )

    payment_table.add_row(
        _("label_possible_impersonation"),
        _("value_yes") if payment_verification["possible_typosquatting"] else _("value_no")
    )

    console.print(payment_table)

    # -------------------------------------------------
    # DETECTED KEYWORDS
    # -------------------------------------------------

    keyword_table = Table(title=_("table_keywords"))

    keyword_table.add_column(_("label_keyword"), style="yellow")

    if keywords:

        for keyword in keywords:

            keyword_table.add_row(keyword)

    else:

        keyword_table.add_row(_("value_none"))

    console.print(keyword_table)

    # -------------------------------------------------
    # RISK ANALYSIS
    # -------------------------------------------------

    analysis = Table(title=_("table_risk_analysis"))

    analysis.add_column(_("label_security_check"), style="cyan")
    analysis.add_column(_("label_result"))

    analysis.add_row(
        _("label_bank"),
        _("value_pass") if verification["verified"] else _("value_fail")
    )

    analysis.add_row(
        _("label_processor"),
        _("value_pass") if payment_verification["verified"] else _("value_fail")
    )

    analysis.add_row(
        "HTTPS",
        _("value_pass") if connection["https"] else _("value_fail")
    )

    if ssl_info["valid"] is True:
        ssl_result = _("value_pass")
    elif ssl_info["valid"] is False:
        ssl_result = _("value_fail")
    else:
        ssl_result = _("value_not_checked")

    analysis.add_row(_("label_ssl_certificate"), ssl_result)

    if domain_info["available"] and domain_info["age_days"] is not None:
        if domain_info["age_days"] < 30:
            age_result = _("value_fail")
        elif domain_info["age_days"] < 180:
            age_result = _("value_warning")
        else:
            age_result = _("value_pass")
    else:
        age_result = _("value_not_checked")

    analysis.add_row(_("label_domain_age"), age_result)

    analysis.add_row(
        _("label_reachable"),
        _("value_pass") if connection["reachable"] else _("value_fail")
    )

    analysis.add_row(
        _("label_possible_impersonation"),
        _("value_detected")
        if (verification["possible_typosquatting"] or payment_verification["possible_typosquatting"])
        else _("value_not_detected")
    )

    analysis.add_row(
        _("label_suspicious_tld"),
        _("value_yes") if suspicious_tld else _("value_no")
    )

    analysis.add_row(
        _("label_detected_keywords"),
        str(len(keywords))
    )

    console.print(analysis)

    # -------------------------------------------------
    # SECURITY SCORE
    # -------------------------------------------------

    console.print(
        Panel.fit(
            f"[bold]{score}/100[/bold]\n"
            f"{_('label_risk_level')}: [{color}]{level}[/{color}]",
            title=_("panel_security_score"),
            border_style=color
        )
    )

    # -------------------------------------------------
    # RECOMMENDATIONS
    # -------------------------------------------------

    recommendations = Text()

    recommendations.append(
        f"{_('table_recommendations')}\n\n",
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
            f"• {_('recommend_verified')}\n"
        )
    else:
        recommendations.append(
            f"• {_('recommend_unverified')}\n"
        )

    if verification["possible_typosquatting"] or payment_verification["possible_typosquatting"]:
        recommendations.append(
            f"• {_('recommend_impersonation')}\n"
        )

    if suspicious_tld:
        recommendations.append(
            "• This website uses a suspicious top-level domain.\n"
        )

    recommendations.append(
        f"• {_('never_share_otp')}\n"
    )

    recommendations.append(
        f"• {_('check_ssl')}\n"
    )

    recommendations.append(
        f"• {_('contact_bank')}\n"
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
            title=_("table_recommendations"),
            border_style="blue"
        )
    )