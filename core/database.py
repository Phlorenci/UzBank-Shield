#Loads the official Uzbek bank database

import json
from pathlib import Path


DATABASE_PATH = Path("data/official_domains.json")


def load_official_domains():
    """
    Load the official bank database.

    Returns:
        dict
    """

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data