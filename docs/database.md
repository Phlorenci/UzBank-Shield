# Official Domain Database

## Overview

The official domain database contains publicly available website domains of licensed commercial banks operating in Uzbekistan.

Its purpose is to help UzBank Shield determine whether a user-provided URL belongs to a verified bank website.

---

## Structure

Each bank entry contains:

- Bank name
- One or more official domains

Example

```json
{
    "name": "Kapitalbank",
    "domains": [
        "kapitalbank.uz"
    ]
}
```

---

## Data Source

Only publicly available information should be added.

Before adding or modifying a domain, verify it using one of the following:

- The bank's official website
- The Central Bank of Uzbekistan

---

## Future Improvements

Future versions may include:

- Official mobile application package names
- Customer support phone numbers
- Official social media accounts
- Bank logo references
- Last verification date