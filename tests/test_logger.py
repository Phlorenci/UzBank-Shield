import logging

from core.logger import setup_logging, log_scan, log_error, log_debug


def test_setup_logging_creates_log_files(tmp_path, monkeypatch):
    monkeypatch.setattr("core.logger.LOG_DIR", tmp_path)
    monkeypatch.setattr("core.logger.SCAN_HISTORY_PATH", tmp_path / "scan_history.log")
    monkeypatch.setattr("core.logger.DEBUG_LOG_PATH", tmp_path / "debug.log")
    monkeypatch.setattr("core.logger._configured", False)

    setup_logging("INFO")

    assert (tmp_path / "scan_history.log").exists()
    assert (tmp_path / "debug.log").exists()


def test_log_scan_writes_entry(tmp_path, monkeypatch):
    monkeypatch.setattr("core.logger.LOG_DIR", tmp_path)
    monkeypatch.setattr("core.logger.SCAN_HISTORY_PATH", tmp_path / "scan_history.log")
    monkeypatch.setattr("core.logger.DEBUG_LOG_PATH", tmp_path / "debug.log")
    monkeypatch.setattr("core.logger._configured", False)

    setup_logging("INFO")
    log_scan("https://kapitalbank.uz", 10, "LOW")

    content = (tmp_path / "scan_history.log").read_text(encoding="utf-8")

    assert "kapitalbank.uz" in content
    assert "10/100" in content
    assert "LOW" in content


def test_log_error_writes_entry(tmp_path, monkeypatch):
    monkeypatch.setattr("core.logger.LOG_DIR", tmp_path)
    monkeypatch.setattr("core.logger.SCAN_HISTORY_PATH", tmp_path / "scan_history.log")
    monkeypatch.setattr("core.logger.DEBUG_LOG_PATH", tmp_path / "debug.log")
    monkeypatch.setattr("core.logger._configured", False)

    setup_logging("DEBUG")
    log_error("Something went wrong")

    content = (tmp_path / "debug.log").read_text(encoding="utf-8")

    assert "ERROR" in content
    assert "Something went wrong" in content


def test_log_debug_respects_log_level(tmp_path, monkeypatch):
    monkeypatch.setattr("core.logger.LOG_DIR", tmp_path)
    monkeypatch.setattr("core.logger.SCAN_HISTORY_PATH", tmp_path / "scan_history.log")
    monkeypatch.setattr("core.logger.DEBUG_LOG_PATH", tmp_path / "debug.log")
    monkeypatch.setattr("core.logger._configured", False)

    setup_logging("INFO")
    log_debug("This should not appear")

    content = (tmp_path / "debug.log").read_text(encoding="utf-8")

    assert "This should not appear" not in content