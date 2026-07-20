from core.banner import print_banner
from core.input_handler import get_user_input
from core.parser import extract_url_components
from core.validator import validate_url
from core.scanner import scan_for_keywords
from core.reporter import print_analysis_report
from core.risk import calculate_risk_score
from core.database import load_official_domains
from core.verifier import verify_domain


def main():
    print_banner()

    url = get_user_input()

    if not validate_url(url):
        print("\nInvalid URL format.")
        return

    components = extract_url_components(url)

    keywords = scan_for_keywords(components)

    score, level = calculate_risk_score(keywords)
    database = load_official_domains()
    verification = verify_domain(
        components["original_url"],
        database
    )

    print_analysis_report(
        components,
        keywords,
        score,
        level,
        verification
    )


if __name__ == "__main__":
    main()