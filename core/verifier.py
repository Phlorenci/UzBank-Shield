from core.similarity import (
    get_domain,
    find_closest_domain
)


def verify_domain(url, database):
    user_domain = get_domain(url)

    for bank in database["banks"]:

        for official_domain in bank["domains"]:

            if user_domain == official_domain.lower():

                return {
                    "verified": True,
                    "bank": bank["name"],
                    "official_domain": official_domain,
                    "closest_domain": official_domain,
                    "similarity": 100.0,
                    "possible_typosquatting": False
                }

    closest = find_closest_domain(
        url,
        database
    )

    if not closest["matched"]:

        return {
            "verified": False,
            "bank": None,
            "official_domain": None,
            "closest_domain": None,
            "similarity": closest["similarity"],
            "possible_typosquatting": False
        }

    return {
        "verified": False,
        "bank": closest["bank"],
        "official_domain": None,
        "closest_domain": closest["domain"],
        "similarity": closest["similarity"],
        "possible_typosquatting": True
    }