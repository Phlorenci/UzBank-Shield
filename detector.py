from core.banner import print_banner
from core.input_handler import get_user_input
from core.validator import validate_url
from core.reporter import print_analysis_report
from core.analyzer import URLAnalyzer


def main():
    print_banner()

    url = get_user_input()

    if not validate_url(url):
        print("\nInvalid URL format.")
        return

    analyzer = URLAnalyzer()

    result = analyzer.analyze(url)

    print_analysis_report(
        result["components"],
        result["keywords"],
        result["score"],
        result["level"],
        result["verification"]
    )


if __name__ == "__main__":
    main()