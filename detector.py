from core.banner import print_banner
from core.input_handler import get_user_input
from core.parser import extract_url_components
from core.validator import validate_url
from core.scanner import scan_for_keywords
from core.reporter import print_analysis_report
from core.risk import calculate_risk_score
from core.database import load_official_domains
from core.verifier import verify_domain
from core.tld import is_suspicious_tld
from core.https_checker import check_https
from core.ssl_checker import check_ssl_certificate
from core.whois_checker import check_domain_info


def main():

    print_banner()

    url = get_user_input()

    if not validate_url(url):

        print("\nInvalid URL format.")
        return

    # ---------------------------------
    # URL analysis
    # ---------------------------------

    components = extract_url_components(url)

    # ---------------------------------
    # Keyword analysis
    # ---------------------------------

    keywords = scan_for_keywords(components)

    # ---------------------------------
    # Official bank verification
    # ---------------------------------

    database = load_official_domains()

    verification = verify_domain(
        components["original_url"],
        database
    )

    # ---------------------------------
    # Suspicious TLD
    # ---------------------------------

    suspicious_tld = is_suspicious_tld(
        components["original_url"]
    )

    # ---------------------------------
    # HTTPS analysis
    # ---------------------------------

    connection = check_https(
        components["original_url"]
    )

    # ---------------------------------
    # SSL verification
    # ---------------------------------

    if connection["https"]:
        ssl_info = check_ssl_certificate(
            components["original_url"]
        )
        
    else:
        ssl_info = {
            "valid": None,
            "issuer": None,
            "expires": None,
            "days_remaining": None,
            "error": "Skipped (HTTP connection)"
        }

    # ---------------------------------
    # Domain information (WHOIS)
    # ---------------------------------

    domain_info = check_domain_info(
        components["domain"]
    )

    # ---------------------------------
    # Risk score
    # ---------------------------------

    score, level = calculate_risk_score(
        keywords,
        verification,
        suspicious_tld,
        connection,
        ssl_info,
        domain_info
    )

    # ---------------------------------
    # Report
    # ---------------------------------

    print_analysis_report(
        components,
        keywords,
        score,
        level,
        verification,
        suspicious_tld,
        connection,
        ssl_info,
        domain_info
    )


if __name__ == "__main__":
    main()