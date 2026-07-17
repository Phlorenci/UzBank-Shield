# Generates the analysis report

def print_analysis_report(components, keywords, score, level):
    """
    Print a formatted URL analysis report.
    """

    print()
    print("=" * 60)
    print("URL SECURITY ANALYSIS REPORT")
    print("=" * 60)

    print("\nOriginal URL")
    print(components["original_url"])

    print("\n" + "-" * 60)

    print("Protocol :", components["protocol"].upper())
    print("Domain   :", components["domain"])
    print("Path     :", components["path"] or "(none)")
    print("Query    :", components["query"] or "(none)")
    print("Fragment :", components["fragment"] or "(none)")

    print("\n" + "-" * 60)

    print("Detected Keywords")

    if keywords:

        for keyword in keywords:
            print(f"✓ {keyword}")

    else:

        print("None")

    print("\n" + "-" * 60)

    print(f"Risk Score : {score}/100")

    if level == "LOW":
        print("Risk Level : LOW")

    elif level == "MEDIUM":
        print("Risk Level : MEDIUM")

    else:
        print("Risk Level : HIGH")

    print("\nRecommendations")

    print("• Verify the official website.")
    print("• Do not enter banking credentials immediately.")
    print("• Check SSL certificate.")
    print("• Compare the domain carefully.")

    print("=" * 60)