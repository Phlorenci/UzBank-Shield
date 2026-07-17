# Generates the analysis report

def print_analysis_report(components, keywords):
    """
    Print a formatted URL analysis report.
    """

    print("\n" + "=" * 60)
    print("URL ANALYSIS REPORT")
    print("=" * 60)

    print(f"Original URL : {components['original_url']}")
    print(f"Protocol     : {components['protocol']}")
    print(f"Domain       : {components['domain']}")
    print(f"Path         : {components['path'] or '(none)'}")
    print(f"Query        : {components['query'] or '(none)'}")
    print(f"Fragment     : {components['fragment'] or '(none)'}")

    print("\nDetected Keywords")

    if keywords:
        for keyword in keywords:
            print(f"{keyword}")
    else:
        print("None")

    print("=" * 60)