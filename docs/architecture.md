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

## Component Responsibilities

| Module | Responsibility |
|---------|----------------|
| Input Handler | Reads user input |
| URL Validator | Checks whether the URL format is valid |
| URL Parser | Extracts protocol, domain, path and query |
| Keyword Scanner | Detects suspicious phishing-related keywords |
| Domain Analysis | Performs additional domain-related checks (planned for Version 1.0) |
| Risk Calculator | Combines detection results into a risk score |
| Report Generator | Formats analysis results |
| Terminal Interface | Displays the final report to the user |

The modular design allows new detection techniques to be added without changing the overall application flow. Future versions will extend the **Domain Analysis** component with SSL verification, domain similarity detection, WHOIS lookups, and official Uzbek bank verification.