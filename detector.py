from core.banner import print_banner
from core.input_handler import get_user_input
from core.parser import extract_url_components
from core.validator import validate_url
from core.scanner import scan_for_keywords
from core.reporter import print_analysis_report


def main():
    print_banner()

    url = get_user_input()

    if not validate_url(url):
        print("\nInvalid URL format.")
        return

    components = extract_url_components(url)

    keywords = scan_for_keywords(components)

    print_analysis_report(
        components,
        keywords
    )


if __name__ == "__main__":
    main()