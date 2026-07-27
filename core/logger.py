"""
Logging setup.

Two independent log files:
- logs/scan_history.log : one line per completed scan (URL, score, level)
- logs/debug.log        : errors, exceptions, and module-level debug info
"""

import logging
from pathlib import Path


LOG_DIR = Path("logs")

SCAN_HISTORY_PATH = LOG_DIR / "scan_history.log"
DEBUG_LOG_PATH = LOG_DIR / "debug.log"

_configured = False


def _ensure_log_dir():
    LOG_DIR.mkdir(exist_ok=True)


def setup_logging(log_level="INFO"):
    """
    Configure both loggers. Safe to call multiple times;
    only configures handlers once per process.
    """

    global _configured

    if _configured:
        return

    _ensure_log_dir()

    # ---------------------------------
    # Scan history logger
    # ---------------------------------

    scan_logger = logging.getLogger("uzbank.scan_history")
    scan_logger.setLevel(logging.INFO)
    scan_logger.propagate = False

    scan_handler = logging.FileHandler(
        SCAN_HISTORY_PATH,
        encoding="utf-8"
    )
    scan_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    scan_logger.addHandler(scan_handler)

    # ---------------------------------
    # Debug/error logger
    # ---------------------------------

    debug_logger = logging.getLogger("uzbank.debug")

    level = getattr(logging, log_level.upper(), logging.INFO)
    debug_logger.setLevel(level)
    debug_logger.propagate = False

    debug_handler = logging.FileHandler(
        DEBUG_LOG_PATH,
        encoding="utf-8"
    )
    debug_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    debug_logger.addHandler(debug_handler)

    _configured = True


def log_scan(url, score, level):
    """
    Record a completed scan in the scan history log.
    """

    scan_logger = logging.getLogger("uzbank.scan_history")
    scan_logger.info(
        f"URL={url} | Score={score}/100 | Level={level}"
    )


def log_error(message, exc_info=False):
    """
    Record an error or exception in the debug log.
    """

    debug_logger = logging.getLogger("uzbank.debug")
    debug_logger.error(message, exc_info=exc_info)


def log_debug(message):
    """
    Record a debug-level trace message.
    """

    debug_logger = logging.getLogger("uzbank.debug")
    debug_logger.debug(message)