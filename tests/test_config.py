import json

from core.config import load_config, DEFAULT_CONFIG


def test_creates_config_on_first_run(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("core.config.CONFIG_PATH", config_path)
    monkeypatch.setattr("builtins.input", lambda _: "2")

    config = load_config()

    assert config["language"] == "ru"
    assert config_path.exists()


def test_loads_existing_config(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"language": "uz", "log_level": "INFO"}))

    monkeypatch.setattr("core.config.CONFIG_PATH", config_path)

    config = load_config()

    assert config["language"] == "uz"


def test_falls_back_on_corrupted_config(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    config_path.write_text("not valid json")

    monkeypatch.setattr("core.config.CONFIG_PATH", config_path)

    config = load_config()

    assert config == DEFAULT_CONFIG


def test_falls_back_on_unsupported_language(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"language": "fr", "log_level": "INFO"}))

    monkeypatch.setattr("core.config.CONFIG_PATH", config_path)

    config = load_config()

    assert config["language"] == "en"


def test_missing_keys_filled_with_defaults(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"language": "ru"}))

    monkeypatch.setattr("core.config.CONFIG_PATH", config_path)

    config = load_config()

    assert config["language"] == "ru"
    assert config["log_level"] == "INFO"