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
    # Risk score
    # ---------------------------------

    score, level = calculate_risk_score(
        keywords,
        verification,
        suspicious_tld,
        connection
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
        connection
    )


if __name__ == "__main__":
    main()