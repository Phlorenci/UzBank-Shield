import argparse

from core.__version__ import __version__
from core.banner import print_banner
from core.input_handler import get_user_input
from core.validator import validate_url
from core.reporter import print_analysis_report
from core.analyzer import URLAnalyzer
from core.config import load_config
from core.logger import setup_logging, log_scan, log_error


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

    analyzer = URLAnalyzer()

    try:
        result = analyzer.analyze(url)

    except Exception as error:
        log_error(f"Analysis failed for {url}: {error}", exc_info=True)
        print("\nAn error occurred while analyzing this URL. Check logs/debug.log for details.")
        return

    log_scan(
        result["components"]["original_url"],
        result["score"],
        result["level"]
    )

    print_analysis_report(
        result["components"],
        result["keywords"],
        result["score"],
        result["level"],
        result["verification"],
        result["suspicious_tld"],
        result["connection"],
        result["ssl_info"],
        result["domain_info"],
        config["language"]
    )


if __name__ == "__main__":
    main()