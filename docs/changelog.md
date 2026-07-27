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