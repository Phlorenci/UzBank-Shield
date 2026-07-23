# Project Architecture

The application follows a modular architecture where each component has a single responsibility.

```text
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
          ┌───────────┴───────────┐
          ▼                       ▼
 Keyword Scanner          Domain Analysis
          │                       │
          └───────────┬───────────┘
                      ▼
              Risk Calculator
                      │
                      ▼
             Report Generator
                      │
                      ▼
             Terminal Interface
```

UzBank Shield

│
├── detector.py
│
├── core
│   ├── banner.py
│   ├── input_handler.py
│   ├── validator.py
│   ├── parser.py
│   ├── scanner.py
│   ├── similarity.py
│   ├── verifier.py
│   ├── tld.py
│   ├── risk.py
│   ├── reporter.py
│   ├── database.py
│   └── theme.py
│
├── database
│   └── banks.json
│
├── tests
│   ├── test_parser.py
│   ├── test_validator.py
│   ├── test_risk.py
│   ├── test_similarity.py
│   ├── test_verifier.py
│   └── test_tld.py
│
└── docs