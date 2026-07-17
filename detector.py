from utils import get_user_input , extract_url_components
"""
==================================================
UzBank Shield
Version 0.2.0

Author: Bobur Mirzarakhimov
GitHub: https://github.com/Phlorenci/UzBank-Shield

Core URL Analysis Engine
==================================================
"""

def print_banner():
    print("=" * 50)
    print("🛡️  UZBANK SHIELD")
    print("Version 0.2.0")
    print("Core URL Analysis Engine")
    print("=" * 50)
    print()
    print("Protect • Detect • Verify")
    print()
    print("Welcome to UzBank Shield!")
    print("This tool analyzes URLs for potential phishing indicators.")
    print("-" * 50)


def main():
    print_banner()

    url = get_user_input()

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