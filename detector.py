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
from core.config import load_config
from core.logger import setup_logging, log_scan, log_error
import argparse
from core.__version__ import __version__

def parse_args():
    parser = argparse.ArgumentParser(
        prog="detector.py",
        description="UzBank Shield - Cybersecurity URL Analysis Toolkit"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"UzBank Shield {__version__}"
    )

    return parser.parse_args()

def main():

    parse_args()

    config = load_config()
    setup_logging(config["log_level"])

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

    try:
        domain_info = check_domain_info(
            components["domain"]
        )
    except Exception as error:
        log_error(f"WHOIS check failed for {components['domain']}: {error}", exc_info=True)
        raise

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
    log_scan(components["original_url"], score, level)

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
        domain_info,
        config["language"]
    )


if __name__ == "__main__":
    main()