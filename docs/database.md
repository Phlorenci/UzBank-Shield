# Official Domain Database

## Overview

UzBank Shield maintains two verified domain databases used to determine whether a user-provided URL belongs to a legitimate financial institution operating in Uzbekistan:

- **`data/official_domains.json`** — licensed commercial banks
- **`data/official_payment_processors.json`** — licensed payment processors and national payment systems

Both databases are consulted during every scan. A URL is checked against each in turn, and the analysis engine reports whether it matches, closely resembles (possible typosquatting), or is unrelated to any known official domain.

---

## Bank Database

### Structure

```json
{
    "version": "1.0.0",
    "country": "Uzbekistan",
    "description": "Verified public domains of licensed commercial banks in Uzbekistan.",
    "last_updated": "2026-07",
    "source": "Central Bank of the Republic of Uzbekistan (cbu.uz) - Head offices of commercial banks",

    "banks": [
        {
            "name": "Kapitalbank",
            "domains": [
                "kapitalbank.uz"
            ]
        }
    ]
}
```

Each bank entry contains:

| Field | Description |
|---|---|
| `name` | The bank's official registered name |
| `domains` | One or more verified official domains. Most banks use a single domain, but the field accepts multiple where applicable. |

The database currently tracks **35 licensed commercial banks**, sourced directly from the Central Bank of Uzbekistan's official registry.

---

## Payment Processor Database

### Structure

```json
{
    "version": "1.0.0",
    "country": "Uzbekistan",
    "description": "Verified public domains of licensed payment processors and payment systems operating in Uzbekistan.",
    "last_updated": "2026-07",
    "source": "Official payment processor websites",

    "processors": [
        {
            "name": "Payme",
            "domains": [
                "payme.uz"
            ]
        }
    ]
}
```

Each processor entry follows the same shape as a bank entry, using `processors` instead of `banks` as the top-level key. This database currently tracks Payme, Click, Uzcard, and Humo.

The two databases are kept separate rather than merged, since banks and payment processors are functionally different categories — this keeps each file's scope unambiguous and avoids conflating the two in reports.

---

## Data Source Standard

Only publicly verifiable information may be added to either database. Before adding or modifying a domain, confirm it using one of the following:

- The institution's own official website
- The Central Bank of Uzbekistan (cbu.uz)

Domains should never be added based on assumption or inference (e.g. guessing that a bank's domain follows a common naming pattern). Several entries in the current database intentionally use non-`.uz` domains (for example, `infinbank.com`) — this is expected and correct where it matches the institution's actual, verified website.

---

## Contributing to the Database

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the general contribution workflow. When submitting a domain addition or correction:

1. Cite the source used to verify the domain in your pull request description
2. Add the entry to the appropriate file (`official_domains.json` for banks, `official_payment_processors.json` for payment processors)
3. Confirm the JSON remains valid and existing tests still pass (`pytest -v`)

---

## Future Improvements

Planned additions to the database schema:

- Official mobile application package names
- Customer support phone numbers
- Official social media accounts
- Bank/processor logo references
- Per-entry last-verification date
- Category/type field, if a third domain category is introduced (see [Roadmap](roadmap.md))