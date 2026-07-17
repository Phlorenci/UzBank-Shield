from core.banner import print_banner
from core.input_handler import get_user_input
from core.parser import extract_url_components
from core.validator import validate_url


def main():
    print_banner()

    url = get_user_input()

    if not validate_url(url):
        print("\nInvalid URL format.")
        print("Please enter a valid URL.")
        return

    components = extract_url_components(url)

    print("\n========== URL COMPONENTS ==========\n")

    print(f"Original URL : {components['original_url']}")
    print(f"Protocol     : {components['protocol']}")
    print(f"Domain       : {components['domain']}")
    print(f"Path         : {components['path'] or '(none)'}")
    print(f"Query        : {components['query'] or '(none)'}")
    print(f"Fragment     : {components['fragment'] or '(none)'}")

    print("\n====================================")


if __name__ == "__main__":
    main()