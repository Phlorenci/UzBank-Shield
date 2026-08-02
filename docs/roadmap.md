# Development Roadmap

This roadmap outlines the planned development of UzBank Shield. Features may change as the project evolves.

---

# Version 0.1 – Project Foundation 

Completed

- Repository setup
- Initial project structure
- Virtual environment
- Basic documentation

---

# Version 0.2 – Core URL Analysis 

Completed

- URL input handling
- URL validation
- URL parser
- Project modularization
- Basic testing

---

# Version 0.3 – Phishing Detection 

Completed

- Keyword detection
- Risk score calculation
- Improved terminal interface
- Analysis reporting
- Documentation improvements

---

# Version 0.4 – Intelligent Bank Verification

Completed

- Official Uzbek bank database
- Official domain matching
- Better bank detection

---

# Version 0.5 – Advanced domain analysis

Completed

- Typosquatting detection
- Homograph detection
- Suspicious TLD detection

---

# Version 0.6 – Website verifcation

Completed

- SSL certificate checks
- WHOIS/domain age
- HTTPS improvements

---

# Version 0.7 – User Experience

Completed

- Uzbek language
- Russian language
- English language
- Configuration file
- Logging (scan history + debug/error logs)

---

# Version 0.7.1 – Full UI Localization

Completed

- Translate table headers and field labels (Property, Value, Status, etc.)
- Translate result values (PASS / FAIL / WARNING / Not Checked)
- Translate remaining recommendation strings (e.g. impersonation warning)
- Translate banner and CLI prompts (input_handler.py, banner.py)
- Review full report output end-to-end in RU and UZ for phrasing/grammar

---

# Version 0.8 – Desktop Application

Completed

- PySide6 GUI
- Scan history
- Settings (language, log-level)
- Structured, sectioned results view

---

# Version 0.9 – Payment Verification

Completed

- Official payment processor database (Payme, Click, Uzcard)
- Payment processor domain verification (mirrors bank verification)
- Typosquat detection extended to payment processors
- Updated reports (terminal + GUI) reflecting payment processor results

---

# Version 1.0 – First Stable Release

Completed

- Complete analysis engine (banks + payment processors)
- Desktop application
- Multilingual support
- Official bank & payment processor verification
- SSL & WHOIS checks
- Documentation

---

# Version 1.1 – Payment Page Safety Checker

Completed

- Analyze payment pages
- Verify trusted payment providers
- Warn before entering bank card information
- Safety recommendations

Note: builds on the payment processor domain verification introduced 
in v0.9. Scope still to be defined — may extend to page-content 
analysis beyond domain verification.

---

# Version 1.2 – QR Code Security

Completed

- Scan QR codes
- Extract URLs
- Analyze destination websites

Note: primarily a GUI feature (camera/image input). Requires a new 
dependency for QR decoding.

---

# Version 1.3 – SMS Scam Detection

Planned

- Analyze SMS messages
- Detect phishing links
- Scam keyword detection

---

# Version 1.4 – AI Security Assistant

Planned

- Explain why a website is suspicious
- Answer user questions
- Recommend actions

---

# Version 1.5 – Community Threat Database

Planned

- Report phishing websites
- Community updates
- Shared threat intelligence

---

# Version 1.6 – Intelligent Domain Suggestions

Planned

- Suggest the closest official bank
- Better typosquatting detection
- Explain similarities

---

# Version 1.7 – Ecosystem

Planned

- Telegram bot (built directly on the core analysis engine — Python, 
  so it inherits every feature above with no extra translation work)
- Browser extension (requires a small backend API server wrapping the 
  analysis engine, since browser JavaScript can't call Python directly)
- Performance improvements

Note: deliberately built last, once the full feature set (v0.9-v1.6) 
is stable — both front-ends then automatically inherit all detection 
capabilities rather than needing to be rebuilt as features are added.

---