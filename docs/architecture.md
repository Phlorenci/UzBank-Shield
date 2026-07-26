# System Architecture

## Overview

UzBank Shield is a modular cybersecurity application designed to detect suspicious banking websites and reduce phishing risks for users in Uzbekistan.

The system analyzes a user-provided URL through several independent security modules. Each module performs a single responsibility, making the project easy to maintain, test, and expand.

---

# Architecture Diagram

```
                   User
                     │
                     ▼
              Input Handler
                     │
                     ▼
              URL Validator
                     │
                     ▼
               URL Parser
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
 Keyword Scanner  TLD Checker  Bank Verifier
         │           │           │
         └───────────┼───────────┘
                     ▼
          Similarity Detection
                     │
                     ▼
            HTTPS Verification
                     │
                     ▼
          SSL Certificate Check
                     │
                     ▼
            WHOIS Information
                     │
                     ▼
              Risk Calculator
                     │
                     ▼
            Analysis Reporter
                     │
                     ▼
                 User Output
```

---

# Project Structure

```
UZBANK-SHIELD
│
├── detector.py
│
├── core
│   ├── banner.py
│   ├── database.py
│   ├── https_checker.py
│   ├── input_handler.py
│   ├── parser.py
│   ├── reporter.py
│   ├── risk.py
│   ├── scanner.py
│   ├── similarity.py
│   ├── ssl_checker.py
│   ├── theme.py
│   ├── tld.py
│   ├── validator.py
│   ├── verifier.py
│   └── whois_checker.py
│
├── data
│   └── official_banks.json
│
├── tests
│   ├── test_https.py
│   ├── test_parser.py
│   ├── test_risk.py
│   ├── test_similarity.py
│   ├── test_tld.py
│   ├── test_validator.py
│   ├── test_verifier.py
│   └── test_whois.py
│
├── docs
│   ├── architecture.md
│   ├── changelog.md
│   ├── database.md
│   └── roadmap.md
│
├── requirements.txt
└── README.md
```

---

# Module Responsibilities

## detector.py

Main application entry point.

Responsibilities:

- Starts the application
- Coordinates all modules
- Executes the security analysis pipeline
- Displays the final report

---

## input_handler.py

Handles user interaction.

Responsibilities:

- Read URL input
- Basic input cleanup

---

## validator.py

Validates the entered URL.

Responsibilities:

- Check URL format
- Reject invalid inputs

---

## parser.py

Extracts URL components.

Responsibilities:

- Protocol
- Domain
- Path
- Query
- Fragment

---

## scanner.py

Performs phishing keyword detection.

Responsibilities:

- Search for suspicious banking keywords
- Return detected keyword list

---

## database.py

Loads the official bank database.

Responsibilities:

- Read official bank domains
- Provide data for verification

---

## verifier.py

Checks whether a website belongs to an official bank.

Responsibilities:

- Exact domain verification
- Official bank identification

---

## similarity.py

Detects possible domain impersonation.

Responsibilities:

- Compare entered domain with official domains
- Calculate similarity percentage
- Detect typosquatting attempts

---

## tld.py

Checks suspicious domain extensions.

Responsibilities:

- Detect unusual TLDs
- Increase phishing risk

---

## https_checker.py

Analyzes website connectivity.

Responsibilities:

- HTTP / HTTPS detection
- Reachability
- HTTP response status

---

## ssl_checker.py

Verifies SSL certificate information.

Responsibilities:

- Certificate validation
- Certificate issuer
- Expiration date
- Remaining validity

---

## whois_checker.py

Retrieves WHOIS domain information.

Responsibilities:

- Registrar information
- Domain creation date
- Domain age
- WHOIS availability

---

## risk.py

Calculates the final phishing risk.

Current factors include:

- Keyword detection
- Official verification
- Domain impersonation
- Suspicious TLD
- HTTPS usage
- SSL certificate
- Website availability

Produces:

- Risk score (0–100)
- Risk level

---

## reporter.py

Generates the terminal report.

Displays:

- Scan summary
- URL information
- HTTPS analysis
- SSL information
- WHOIS information
- Official verification
- Keyword detection
- Risk analysis
- Recommendations

---

## banner.py

Displays the project banner and startup information.

---

## theme.py

Provides Rich console styling.

---

# Testing

The project uses **pytest** for automated testing.

Current test coverage includes:

- URL validation
- URL parsing
- Risk calculation
- HTTPS analysis
- Similarity detection
- TLD detection
- Bank verification
- WHOIS analysis

---

# Design Principles

The project follows several software engineering principles:

- Modular architecture
- Single Responsibility Principle (SRP)
- Separation of concerns
- Reusable components
- Test-driven development
- Easy future extensibility

---

# Future Architecture

Future versions may introduce additional modules, including:

- Browser Extension
- Telegram Bot
- Desktop Application
- Payment Page Scanner
- QR Code Verification
- Anti-Scam Detection Engine
- AI-based Phishing Detection

These components will reuse the existing security analysis modules without major architectural changes.