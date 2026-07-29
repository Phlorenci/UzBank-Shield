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

---