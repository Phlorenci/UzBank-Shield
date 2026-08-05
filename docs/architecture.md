# System Architecture

## Overview

UzBank Shield is a modular cybersecurity application designed to detect suspicious banking and payment-processor websites, reducing phishing risk for users in Uzbekistan.

The system is built around a single shared analysis engine (`URLAnalyzer`) that runs a URL through several independent security checks. Two front-ends — a terminal application and a PySide6 desktop GUI — both call this same engine and differ only in how they present results. This separation means any improvement to the analysis logic automatically benefits both interfaces without duplicated code.

---

# Architecture Diagram

User
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    Terminal App              Desktop GUI
    (detector.py)               (gui.py)
          │                       │
          └───────────┬───────────┘
                       ▼
                 URLAnalyzer
                (core/analyzer.py)
                       │
                       ▼
                  URL Parser
                       │
     ▼           ▼           ▼
 Keyword Scanner  TLD Checker  Bank Verifier
         │           │           │
         │           │        Payment Processor
         │           │            Verifier
         │           │              │
         │           │       Payment Page Analyzer
         │           │              │
         └───────────┼──────────────┘
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
Structured Result Dict
│
┌────────────┴────────────┐
▼ ▼
Terminal Reporter GUI Results View
(core/reporter.py) (gui.py)

---

# Project Structure

UZBANK-SHIELD
│
├── detector.py
├── gui.py
│
├── gui
│   ├── __init__.py
│   ├── settings_dialog.py
│   ├── qr_scanner_dialog.py
│   ├── message_analyzer_dialog.py
│   └── ai_assistant_dialog.py
│
├── core
│   ├── analyzer.py
│   ├── ai_assistant.py
│   ├── banner.py
│   ├── config.py
│   ├── database.py
│   ├── https_checker.py
│   ├── input_handler.py
│   ├── logger.py
│   ├── messages.py
│   ├── page_analyzer.py
│   ├── parser.py
│   ├── payment_verifier.py
│   ├── qr_classifier.py
│   ├── qr_safety.py
│   ├── qr_scanner.py
│   ├── qr_worker.py
│   ├── reporter.py
│   ├── risk.py
│   ├── scanner.py
│   ├── similarity.py
│   ├── sms_analyzer.py
│   ├── ssl_checker.py
│   ├── theme.py
│   ├── tld.py
│   ├── validator.py
│   ├── verifier.py
│   ├── whois_checker.py
│   └── __version__.py
│
├── data
│   ├── official_domains.json
│   ├── official_payment_processors.json
│   └── sms_scam_patterns.json
│
├── assets
│   ├── logo.svg
│   ├── logo.png
│   ├── uzbank_shield_logo.ico
│   └── screenshots/
│
├── logs
│   ├── scan_history.log
│   └── debug.log
│
├── tests
│   └── test_*.py  (30+ test files)
│
├── docs
│   ├── architecture.md
│   ├── changelog.md
│   ├── database.md
│   └── roadmap.md
│
├── .github
│   └── workflows
│       └── tests.yml
│
├── config.json.default
├── requirements.txt
├── CONTRIBUTING.md
└── README.md 

---

# Module Responsibilities

## detector.py

Terminal application entry point.

Responsibilities:

- Parses CLI arguments (`--version`, `--help`)
- Loads configuration and initializes logging
- Reads user input, calls `URLAnalyzer`
- Passes the result to `core/reporter.py` for display

---

## gui.py / gui/

Desktop application entry point (PySide6) and its dialog modules.

**gui.py** — main window: URL input, results display, scan history, toolbar
**gui/settings_dialog.py** — language, log level, OpenAI API key
**gui/qr_scanner_dialog.py** — live webcam QR/barcode scanning
**gui/message_analyzer_dialog.py** — SMS/message scam analysis
**gui/ai_assistant_dialog.py** — AI Security Assistant chat

Responsibilities:

- Builds the main window, results view, and scan history list
- Runs scans on a background thread (`QThread` + worker object) to keep the UI responsive during network I/O
- Provides a Settings dialog for language, log level, and OpenAI API key, including first-run setup on a fresh install
- Applies the app's dark theme and window icon

---

## core/analyzer.py

The shared analysis engine used by both front-ends.

Responsibilities:

- Runs the complete scan pipeline: parsing, keyword scanning, bank verification, payment processor verification, TLD check, HTTPS/SSL check, WHOIS lookup, and risk scoring
- Returns a single structured result dict, with no printing or presentation logic of its own
- Performs real network I/O (HTTPS, SSL, WHOIS), so callers on a UI thread should run it in the background

---

## core/input_handler.py

Handles terminal user interaction.

Responsibilities:

- Read URL input
- Basic input cleanup

---

## core/validator.py

Validates the entered URL.

Responsibilities:

- Check URL format
- Reject invalid inputs

---

## core/parser.py

Extracts URL components.

Responsibilities:

- Protocol, domain, path, query, fragment

---

## core/scanner.py

Performs phishing keyword detection.

Responsibilities:

- Search for suspicious banking keywords
- Return detected keyword list

---

## core/database.py

Loads the official bank database.

Responsibilities:

- Read official bank domains (`data/official_domains.json`)
- Provide data for bank verification

---

## core/verifier.py

Checks whether a website belongs to an official bank.

Responsibilities:

- Exact domain verification
- Official bank identification

---

## core/payment_verifier.py

Checks whether a website belongs to an official payment processor. Mirrors `core/database.py` + `core/verifier.py`'s pattern, applied to a separate category.

Responsibilities:

- Load the payment processor database (`data/official_payment_processors.json`)
- Exact domain verification and typosquat detection for payment processors (Payme, Click, Uzcard, Humo)

---

## core/page_analyzer.py

Analyzes a payment page's HTML content, independent of domain verification.

Responsibilities:

- Fetch the page and parse its HTML
- Detect form fields commonly used to collect card information
- Fail safe on network errors or non-200 responses, since this is a 
  bonus signal rather than a required check

## core/similarity.py

Detects possible domain impersonation.

Responsibilities:

- Compare entered domain with official domains
- Calculate similarity percentage
- Detect typosquatting attempts

---

## core/tld.py

Checks suspicious domain extensions.

Responsibilities:

- Detect unusual TLDs
- Increase phishing risk

---

## core/https_checker.py

Analyzes website connectivity.

Responsibilities:

- HTTP / HTTPS detection
- Reachability
- HTTP response status

---

## core/ssl_checker.py

Verifies SSL certificate information.

Responsibilities:

- Certificate validation
- Certificate issuer
- Expiration date
- Remaining validity

---

## core/whois_checker.py

Retrieves WHOIS domain information.

Responsibilities:

- Registrar information
- Domain creation date
- Domain age
- WHOIS availability

---

## core/risk.py

Calculates the final phishing risk.

Factors include:

- Keyword detection
- Official bank verification
- Official payment processor verification
- Domain impersonation (bank or payment processor)
- Suspicious TLD
- HTTPS usage
- SSL certificate
- Website availability
- Domain age

Produces:

- Risk score (0–100)
- Risk level (LOW / MEDIUM / HIGH)

---

## core/reporter.py

Generates the terminal report.

Displays:

- Scan summary
- URL information
- HTTPS analysis
- SSL information
- WHOIS information
- Official bank verification
- Official payment processor verification
- Keyword detection
- Risk analysis
- Recommendations (language-aware)

---

## core/config.py

Manages persistent configuration.

Responsibilities:

- First-run interactive language setup (terminal) or dialog-based setup (GUI)
- Load, validate, and save `config.json`
- Fall back to safe defaults if the config file is missing or corrupted

---

## core/messages.py

Provides multilingual message strings.

Responsibilities:

- Look up user-facing strings by key and language (English, Russian, Uzbek)
- Fall back to English if a translation is missing

---

## core/logger.py

Manages application logging.

Responsibilities:

- Scan history log (`logs/scan_history.log`) — one line per scan
- Debug/error log (`logs/debug.log`) — exceptions and diagnostic detail

---

## core/banner.py

Displays the terminal banner and startup information.

---

## core/theme.py

Provides the shared Rich console instance used for terminal styling.

---

# Testing

The project uses **pytest** for automated testing, with 66+ tests covering:

- URL validation and parsing
- Risk calculation (including payment processor scoring)
- HTTPS, SSL, and WHOIS analysis
- Similarity and typosquat detection
- Bank and payment processor verification
- Configuration loading (first-run, corrupted file, missing keys)
- Multilingual message lookup
- Logging (scan history and debug logs)
- CLI flags (`--version`, `--help`)
- Full `URLAnalyzer` pipeline (structural, integration, and mocked wiring tests)

---

# Design Principles

The project follows several software engineering principles:

- Modular architecture with a single shared analysis engine
- Single Responsibility Principle (SRP)
- Separation of logic from presentation (engine vs. terminal/GUI front-ends)
- Reusable components
- Test-driven development
- Easy future extensibility

---

# Future Architecture

Planned extensions (see [Roadmap](roadmap.md) for full detail):

- **v1.1 Payment Page Safety Checker** — extends beyond domain verification into page-content analysis
- **v1.2 QR Code Security** — new GUI-side image/camera input path
- **v1.3 SMS Scam Detection** — reusable detection logic shared with the future Telegram bot
- **v1.4 AI Security Assistant** — LLM API integration
- **v1.5 Community Threat Database** — first component requiring a backend server and database
- **v1.6 Intelligent Domain Suggestions** — extends the existing similarity engine
- **v1.7 Ecosystem** — Telegram bot (built directly on `URLAnalyzer`) and browser extension (requires a small backend API server, since browser JavaScript cannot call Python directly)

These components are designed to build on the existing `URLAnalyzer` engine rather than requiring architectural changes to the core.