#python-whois returns inconsistent shapes across TLDs —
# creation_date can be a datetime, a list of datetimes,
# or (rarely) a string, and registrar can be a string or list.
# The two _normalize_* helpers absorb that mess.
#It follows the same defensive try/except pattern as your ssl_checker.py,
# returning a consistent dict shape either way instead of raising.
#.uz domains may have limited or no public WHOIS data (common for ccTLDs) —
# that's handled as available: False rather than crashing.


from datetime import datetime

import whois

def _strip_timezone(value):
    # WHOIS servers inconsistently return naive or timezone-aware
    # datetimes. Normalize to naive UTC-ish local time so date math
    # against datetime.now() never raises.
    if value.tzinfo is not None:
        return value.replace(tzinfo=None)

    return value


def _normalize_creation_date(creation_date):
    # python-whois sometimes returns a single value and
    # sometimes a list of values (one per WHOIS record).
    if isinstance(creation_date, list):
        creation_date = creation_date[0] if creation_date else None

    if isinstance(creation_date, datetime):
        return _strip_timezone(creation_date)

    if isinstance(creation_date, str):
        for date_format in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d-%m-%Y"):
            try:
                return datetime.strptime(creation_date, date_format)
            except ValueError:
                continue

    return None


def _normalize_registrar(registrar):
    # Some registries also return the registrar as a list.
    if isinstance(registrar, list):
        registrar = registrar[0] if registrar else None

    if isinstance(registrar, str) and registrar.strip():
        return registrar.strip()

    return None


def check_domain_info(domain):
    if domain.startswith("http://"):
        domain = domain.replace("http://", "")

    if domain.startswith("https://"):
        domain = domain.replace("https://", "")

    domain = domain.split("/")[0]

    try:
        record = whois.whois(domain)

    except Exception as error:

        return {
            "available": False,
            "registrar": None,
            "created": None,
            "age_days": None,
            "error": str(error)
        }

    created = _normalize_creation_date(
        record.get("creation_date")
    )

    registrar = _normalize_registrar(
        record.get("registrar")
    )

    if created is None and registrar is None:

        return {
            "available": False,
            "registrar": None,
            "created": None,
            "age_days": None,
            "error": "No WHOIS data returned"
        }

    age_days = (
        (datetime.now() - created).days
        if created is not None
        else None
    )

    return {
        "available": True,
        "registrar": registrar or "Unknown",
        "created": created.strftime("%Y-%m-%d") if created else None,
        "age_days": age_days,
        "error": None
    }