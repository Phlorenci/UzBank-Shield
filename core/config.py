import json
from pathlib import Path

from core.theme import console


CONFIG_PATH = Path("config.json")

SUPPORTED_LANGUAGES = {
    "1": "en",
    "2": "ru",
    "3": "uz"
}

LANGUAGE_NAMES = {
    "en": "English",
    "ru": "Russian",
    "uz": "Uzbek"
}

DEFAULT_CONFIG = {
    "language": "en",
    "log_level": "INFO"
}


def _prompt_language():

    console.print("\n[bold cyan]First-time setup[/bold cyan]")
    console.print("Choose your language / Выберите язык / Tilni tanlang:\n")
    console.print("  1) English")
    console.print("  2) Russian (Русский)")
    console.print("  3) Uzbek (O'zbek)")

    while True:
        choice = input("\nEnter a number (1-3): ").strip()

        if choice in SUPPORTED_LANGUAGES:
            return SUPPORTED_LANGUAGES[choice]

        console.print("[red]Invalid choice. Please enter 1, 2, or 3.[/red]")


def _write_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)


def _run_first_time_setup():
    language = _prompt_language()

    config = dict(DEFAULT_CONFIG)
    config["language"] = language

    _write_config(config)

    console.print(
        f"\n[green]Language set to {LANGUAGE_NAMES[language]}.[/green] "
        f"You can change this later by editing config.json.\n"
    )

    return config


def load_config():
    if not CONFIG_PATH.exists():
        return _run_first_time_setup()

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            config = json.load(file)

    except (json.JSONDecodeError, OSError):
        console.print(
            "[yellow]Warning: config.json is invalid. Using defaults.[/yellow]"
        )
        return dict(DEFAULT_CONFIG)
    
    merged = dict(DEFAULT_CONFIG)
    merged.update(config)

    if merged["language"] not in LANGUAGE_NAMES:
        console.print(
            "[yellow]Warning: unsupported language in config.json. "
            "Falling back to English.[/yellow]"
        )
        merged["language"] = "en"

    return merged

def save_config(config):
    #Persist a config dict to disk. Used by any caller (terminal or GUI) that wants to update settings outside of first-time setup

    merged = dict(DEFAULT_CONFIG)
    merged.update(config)

    _write_config(merged)

    return merged