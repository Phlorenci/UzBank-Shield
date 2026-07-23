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


def main():

    print_banner()

    url = get_user_input()

    if not validate_url(url):

        print("\nInvalid URL format.")
        return

    components = extract_url_components(url)

    keywords = scan_for_keywords(components)

    database = load_official_domains()

    verification = verify_domain(
        components["original_url"],
        database
    )

    suspicious_tld = is_suspicious_tld(
        components["original_url"]
    )

    score, level = calculate_risk_score(
        keywords,
        verification,
        suspicious_tld
    )

    print_analysis_report(
        components,
        keywords,
        score,
        level,
        verification,
        suspicious_tld
    )


if __name__ == "__main__":
    main()