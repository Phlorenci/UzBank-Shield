from difflib import SequenceMatcher
from urllib.parse import urlparse

SIMILARITY_THRESHOLD = 80


def calculate_similarity(domain1, domain2):
    similarity = SequenceMatcher(
        None,
        domain1.lower(),
        domain2.lower()
    ).ratio()

    return round(similarity * 100, 2)


def get_domain(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return urlparse(url).netloc.lower()


def find_closest_domain(url, database):
    user_domain = get_domain(url)

    best_match = None
    highest_similarity = 0

    for bank in database["banks"]:

        for official_domain in bank["domains"]:

            similarity = calculate_similarity(
                user_domain,
                official_domain
            )

            if similarity > highest_similarity:

                highest_similarity = similarity

                best_match = {
                    "bank": bank["name"],
                    "domain": official_domain,
                    "similarity": similarity
                }

    if highest_similarity < SIMILARITY_THRESHOLD:

        return {
            "bank": None,
            "domain": None,
            "similarity": highest_similarity,
            "matched": False
        }

    best_match["matched"] = True

    return best_match