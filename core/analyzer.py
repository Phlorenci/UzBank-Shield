from core.parser import extract_url_components
from core.scanner import scan_for_keywords
from core.database import load_official_domains
from core.verifier import verify_domain
from core.risk import calculate_risk_score


class URLAnalyzer:
    def analyze(self, url):
        # Parse URL
        components = extract_url_components(url)

        # Scan keywords
        keywords = scan_for_keywords(components)

        # Load database
        database = load_official_domains()

        # Verify domain
        verification = verify_domain(
            components["original_url"],
            database
        )

        # Calculate risk
        score, level = calculate_risk_score(
            keywords,
            verification
        )

        return {
            "components": components,
            "keywords": keywords,
            "verification": verification,
            "score": score,
            "level": level
        }