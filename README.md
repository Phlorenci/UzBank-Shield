# UzBank Shield

UzBank Shield is an open-source Python project that analyzes URLs for common phishing indicators. The project is being developed to explore practical cybersecurity techniques while focusing on online banking safety in Uzbekistan.

Rather than trying to detect every type of cyber threat, the current goal is to identify suspicious banking-related URLs using simple and understandable detection methods. The project will gradually expand with more advanced security checks as development continues.

---

## Why this project?

Online banking scams have become increasingly common. Attackers often create fake websites that closely resemble legitimate bank pages in order to steal passwords, card details, and SMS verification codes.

UzBank Shield was started as a personal cybersecurity learning project with the long-term goal of helping users recognize suspicious banking websites before entering sensitive information.

---

## Current Features

Current version: **v0.4.0**

- URL parsing and validation
- Phishing keyword detection
- Risk score calculation
- Official Uzbek bank domain verification
- Security recommendations
- Modular project architecture

---

## Project Structure

```text
UzBank-Shield
│
├── core/
│   ├── banner.py
│   ├── input_handler.py
│   ├── parser.py
│   ├── reporter.py
│   ├── risk.py
│   ├── scanner.py
│   ├── theme.py
│   └── validator.py
│
├── data/
│   └── phishing_keywords.json
│
├── docs/
│
├── tests/
│
├── assets/
│
├── detector.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/Phlorenci/UzBank-Shield.git
```

Open the project.

```bash
cd UzBank-Shield
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
python -m pip install -r requirements.txt
```

Run the application.

```bash
python detector.py
```

---

## Example

Input

```
https://kapitalbank-login.uz/reset-password
```

Output

```
Risk Score : 60/100

Detected keywords

login
bank
reset
password
```

---

## Roadmap

## Documentation

-  [Roadmap](docs/roadmap.md)
-  [Architecture](docs/architecture.md)
-  [Changelog](docs/changelog.md)
-  [Database](docs/database.md)

---

### Future Development

Long-term plans include:

- Desktop application
- Telegram bot
- Browser extension
- Android application
- Uzbek, Russian and English interface

---

## Disclaimer

UzBank Shield is an educational and research project.

Analysis results should not be considered professional security advice or a guarantee that a website is safe or malicious.

---

## Author

Bobur Mirzarakhimov

Computer Science Student

Sejong University

GitHub

https://github.com/Phlorenci

---

## License

MIT License