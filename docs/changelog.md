# Changelog

## v0.3.0

### Added

- URL validation
- URL parser
- Phishing keyword detection
- Risk score calculation
- Improved terminal interface
- Rich library integration

---

## Version 0.4.0

### Added

- Official Uzbek bank domain database
- Official domain verification engine
- Domain verification reporting
- Bank identification
- Improved security recommendations

### Improved

- Analysis report layout
- Project architecture
- Verification workflow

## Version 0.5

### Added

- Domain similarity engine
- Intelligent bank verification
- Typosquatting detection
- Suspicious TLD detection

### Improved

- Risk analysis algorithm
- Terminal security report
- Recommendations

### Testing

- Added unit tests for similarity
- Added unit tests for verifier
- Added unit tests for TLD detection

---

## Version 0.6

### Added

- HTTPS protocol analysis
- Website reachability checks
- SSL certificate verification
- SSL expiration analysis

### Improved

- Risk score calculation
- Security report
- User recommendations

### Testing

- Added HTTPS tests
- Updated risk score tests

---

## Version 0.7

### Added

- Configuration system (`config.json`) with first-run setup
- Interactive language selection on first run (English, Russian, Uzbek)
- Multilingual message support for verification status and recommendations
- Scan history logging (`logs/scan_history.log`)
- Debug/error logging (`logs/debug.log`)

### Improved

- `detector.py` now loads config and initializes logging on startup
- Error handling around WHOIS checks now logs failures instead of failing silently

### Testing

- Added unit tests for config loading (first-run, corrupted file, missing keys)
- Added unit tests for multilingual message lookup
- Added unit tests for scan and debug logging

### Known Limitations

- Translations currently cover verification status and security recommendations only. Table headers, field labels, and result values (e.g. "PASS"/"FAIL") remain English-only. Full UI translation is tracked for a future release — see [Roadmap](roadmap.md).

---

## Version 0.8

### Added

- PySide6 desktop GUI (`gui.py`) as a second front-end alongside the terminal app
- Structured, sectioned results view (score, verification, connection/SSL, WHOIS, keywords)
- Background-threaded scanning so the GUI stays responsive during network checks
- Session-based scan history with clickable past results
- In-app Settings dialog (language, log level), including automatic first-run setup on fresh installs
- `URLAnalyzer` extended to run the complete analysis pipeline, returning one structured result shared by both the terminal app and the GUI

### Improved

- `detector.py` refactored to use `URLAnalyzer` instead of duplicating pipeline logic
- `core/config.py` gained a `save_config()` function so settings can be updated outside of first-run setup
- Verification status label in the GUI respects the configured language

### Testing

- Added `tests/test_analyzer.py` covering the full pipeline (structural, integration, and mocked wiring tests)
- 56 tests passing total

### Known Limitations

- GUI language support currently covers verification status only, matching the same scope limitation tracked in the v0.7.1 Full UI Localization milestone
- Scan history is session-only and not persisted to disk between app launches

### Improved
- Official bank database expanded from 5 to 35 banks, sourced directlyfrom the Central Bank of Uzbekistan's official registry

---

Dark theme + app icon addition — this shipped as its own commit after the v0.8 changelog entry was written, so it's likely missing entirely. Worth a small "Improved" note under v0.8, or its own tiny v0.8.x mention.

35-bank expansion — check whether this got folded into the v0.9 entry already or needs to sit separately under v0.8 (it happened between the two, timing-wise)

---

## Version 0.9

### Added
- Official payment processor database (data/official_payment_processors.json): 
  Payme, Click, Uzcard, Humo
- core/payment_verifier.py — payment processor domain verification, 
  mirroring the existing bank verifier pattern
- Payment processor verification integrated into risk scoring
- New "Official Payment Processor Verification" section in terminal 
  and GUI reports

### Improved
- Official bank database expanded from 5 to 35 banks, sourced directly 
  from the Central Bank of Uzbekistan's official registry

### Testing
- Added tests/test_payment_verifier.py (6 tests)
- Updated test_risk.py and test_analyzer.py for new signatures
- 66 tests passing total

---

## Version 1.1

### Added
- Payment page content analysis (core/page_analyzer.py): fetches a 
  page's HTML and detects fields commonly used to collect card 
  information (card number, CVV, expiry, cardholder name)
- New risk factor: pages requesting card details on an unverified 
  domain (not a known bank or payment processor) add significant 
  risk weight to the score
- New "Payment Page Analysis" section in terminal and GUI reports
- Translated warning message shown when card info is requested on an 
  unverified domain (English, Russian, Uzbek)

### Testing
- Added tests/test_page_analyzer.py (4 tests): card field detection, 
  no false positives on unrelated forms, safe failure on network 
  errors, safe failure on bad HTTP status
- Added 2 new risk-scoring tests confirming the card warning only 
  triggers on unverified domains
- 72 tests passing total

### Dependencies
- Added beautifulsoup4 for HTML parsing

---

## Version 1.2

### Added
- Live QR code and barcode scanning (desktop GUI): webcam capture, 
  automatic decoding, and content classification
- QR/barcode content classification: distinguishes website URLs, 
  WiFi credentials, contact cards, email/phone links, cryptocurrency 
  addresses, EMV payment QR codes (Toss, Alipay, WeChat Pay, and 
  similar), retail barcodes, and generic numeric reference codes
- Safety assessment for each QR/barcode type (e.g. open WiFi warning, 
  payment QR merchant verification prompt, crypto address warning)
- Website URL QR codes automatically route through the full 
  URLAnalyzer scan pipeline; all other types show an in-dialog 
  classification and safety summary

### Fixed
- GUI language switching previously only affected the terminal app — 
  the desktop GUI stayed in English regardless of the configured 
  language. The entire GUI (main window, results panel, Settings 
  dialog, QR scanner dialog, risk level labels, and all field values) 
  now correctly re-translates live when the language is changed in 
  Settings
- Fixed a QFormLayout bug where empty-string row labels prevented 
  Settings dialog fields from being retranslatable
- Removed noisy zbar/PDF417 decoder warnings by restricting barcode 
  scanning to relevant symbologies (QR, EAN, UPC, Code128, Code39)

### Testing
- Added tests/test_qr_scanner.py, test_qr_classifier.py, test_qr_safety.py
- 80+ tests passing total

### Dependencies
- Added opencv-python, pyzbar (QR/barcode scanning)
- Added qrcode, Pillow (test-time QR image generation)

---

## Version 1.3

### Added
- SMS/message scam analysis (desktop GUI): paste any message text 
  to extract and analyze URLs, and scan for scam indicators
- Multilingual scam phrase detection (English, Russian, Uzbek) across 
  four categories: urgency, sensitive info requests, too-good-to-be-true 
  claims, and fake authority
- Institution impersonation detection: flags messages claiming to be 
  from a real bank/payment processor when the linked domain doesn't 
  match their actual verified domain
- Generic time-pressure detection (regex-based): catches urgency 
  framed around any time limit, not just pre-written phrases
- Structural heuristics: detects the general shape of phishing SMS 
  (short message + link + call-to-action verb) even without any 
  specific trigger phrase
- Full localization of SMS analysis results (EN/RU/UZ)

### Testing
- Added tests/test_sms_analyzer.py covering URL extraction, pattern 
  matching, impersonation detection, time-pressure regex, structural 
  heuristics, and combined risk assessment
- 100+ tests passing total

---

## Version 1.4

### Added
- AI Security Assistant (desktop GUI): chat interface for asking 
  security/phishing questions, automatically grounded in the current 
  scan result when one exists
- Bring-your-own-key design (OpenAI): no shared API key, no cost to 
  the project, avoids the abuse/leaked-key risks of an embedded key
- System-prompt scoping keeps the assistant focused on security 
  topics rather than open-ended general chat
- Full localization of the assistant dialog (EN/RU/UZ)

### Testing
- Added tests/test_ai_assistant.py: error handling, context 
  formatting, mocked API success/failure paths
- 100+ tests passing total

### Dependencies
- Added openai