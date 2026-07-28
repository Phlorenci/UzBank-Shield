import subprocess
import sys


def test_version_flag_prints_version_and_exits():
    result = subprocess.run(
        [sys.executable, "detector.py", "--version"],
        capture_output=True,
        text=True
    )

    assert "UzBank Shield" in result.stdout
    assert result.returncode == 0


def test_help_flag_prints_usage_and_exits():
    result = subprocess.run(
        [sys.executable, "detector.py", "--help"],
        capture_output=True,
        text=True
    )

    assert "usage:" in result.stdout.lower()
    assert result.returncode == 0