import json
from pathlib import Path


DATABASE_PATH = Path("data/official_domains.json")


def load_official_domains():
    # Check if the database file exists
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Official domain database not found: {DATABASE_PATH}"
        )

    # Read JSON safely
    try:
        with open(DATABASE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in database file.\n{error}"
        )

    # Validate structure
    required_fields = [
        "version",
        "country",
        "banks"
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(
                f"Database is missing required field: '{field}'"
            )

    if not isinstance(data["banks"], list):
        raise ValueError(
            "'banks' must be a list."
        )

    return data