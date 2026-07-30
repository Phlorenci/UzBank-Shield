from core.parser import extract_url_components
from core.scanner import scan_for_keywords
from core.database import load_official_domains
from core.verifier import verify_domain
from core.tld import is_suspicious_tld
from core.https_checker import check_https
from core.ssl_checker import check_ssl_certificate
from core.whois_checker import check_domain_info
from core.risk import calculate_risk_score
from core.payment_verifier import load_payment_processors, verify_payment_processor


class URLAnalyzer:

    def analyze(self, url):
        # ---------------------------------
        # URL parsing
        # ---------------------------------

        components = extract_url_components(url)

        # ---------------------------------
        # Keyword analysis
        # ---------------------------------

        keywords = scan_for_keywords(components)

        # ---------------------------------
        # Official bank verification
        # ---------------------------------

        database = load_official_domains()

        verification = verify_domain(
            components["original_url"],
            database
        )

        # ---------------------------------
        # Official payment processor verification
        # ---------------------------------

        payment_database = load_payment_processors()

        payment_verification = verify_payment_processor(
            components["original_url"],
            payment_database
        )

        # ---------------------------------
        # Suspicious TLD
        # ---------------------------------

        suspicious_tld = is_suspicious_tld(
            components["original_url"]
        )

        # ---------------------------------
        # HTTPS analysis
        # ---------------------------------

        connection = check_https(
            components["original_url"]
        )

        # ---------------------------------
        # SSL verification
        # ---------------------------------

        if connection["https"]:
            ssl_info = check_ssl_certificate(
                components["original_url"]
            )

        else:
            ssl_info = {
                "valid": None,
                "issuer": None,
                "expires": None,
                "days_remaining": None,
                "error": "Skipped (HTTP connection)"
            }

        # ---------------------------------
        # Domain information (WHOIS)
        # ---------------------------------

        domain_info = check_domain_info(
            components["domain"]
        )

        # ---------------------------------
        # Risk score
        # ---------------------------------

        score, level = calculate_risk_score(
            keywords,
            verification,
            payment_verification,
            suspicious_tld,
            connection,
            ssl_info,
            domain_info,
        )

        # ---------------------------------
        # Structured result
        # ---------------------------------

        return {
            "components": components,
            "keywords": keywords,
            "verification": verification,
            "payment_verification": payment_verification,
            "suspicious_tld": suspicious_tld,
            "connection": connection,
            "ssl_info": ssl_info,
            "domain_info": domain_info,
            "score": score,
            "level": level,
        }