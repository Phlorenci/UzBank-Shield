# Contributing to UzBank Shield

Thanks for your interest in contributing! UzBank Shield is an educational cybersecurity project focused on detecting phishing attempts against Uzbek banking websites. Contributions of all sizes are welcome — bug fixes, new checks, translations, documentation, and tests.

---

## Getting Started

1. **Fork the repository** and clone your fork:

```bash
   git clone https://github.com/<your-username>/UzBank-Shield.git
   cd UzBank-Shield
```

2. **Create a virtual environment:**

```bash
   python -m venv .venv
```

3. **Activate it:**

   Windows:
```bash
   .venv\Scripts\activate
```

   macOS/Linux:
```bash
   source .venv/bin/activate
```

4. **Install dependencies:**

```bash
   python -m pip install -r requirements.txt
```

5. **Run the test suite** to confirm everything works before you start:

```bash
   pytest -v
```

---

## Branching

Create a new branch off `main` for every change — don't commit directly to `main`.

Use a prefix that describes the type of change:

| Prefix         | Use for                                      |
|----------------|-----------------------------------------------|
| `feature/`     | New functionality                              |
| `fix/`         | Bug fixes                                      |
| `docs/`        | Documentation-only changes                     |
| `tests/`       | Test additions or fixes with no behavior change |
| `assets/`      | Images, logos, or other static assets          |

Example:

```bash
git checkout -b feature/telegram-bot-notifications
```

---

## Code Style

- Follow the existing modular structure — one responsibility per file under `core/`.
- Keep functions small and readable; prefer clear code over clever code.
- Match the existing formatting style (blank lines between logical blocks, docstrings on public functions).
- Add a short comment or docstring explaining *why*, not just *what*, when the logic isn't obvious.

---

## Testing

- Every new feature or bug fix should include at least one test in `tests/`.
- Tests use `pytest`. Name test files `test_<module>.py` and test functions `test_<behavior>`.
- Run the full suite before opening a PR:

```bash
   pytest -v
```

- All tests must pass before a PR will be merged.

---

## Commit Messages

Keep commit messages short and descriptive. Reference the related issue number when one exists: