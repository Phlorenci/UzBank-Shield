from utils import get_user_input
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

    print("\n URL received successfully!")
    print(f"Input: {url}")


if __name__ == "__main__":
    main()