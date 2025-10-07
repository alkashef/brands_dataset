"""Logging utilities for the brandgen package."""

from __future__ import annotations
import logging
import sys
import time
from pathlib import Path


_START_TIME = time.time()


class _ElapsedFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        elapsed = record.created - _START_TIME
        record.elapsed = f"{elapsed:8.2f}s"  # type: ignore[attr-defined]
        return super().format(record)


def configure_logger(name: str = "brandgen", level: int = logging.INFO, log_file: str | None = None) -> logging.Logger:
    """Configure and return a package logger with stdout + optional file handler."""
    logger = logging.getLogger(name)
    if logger.handlers:  # Already configured
        return logger
    logger.setLevel(level)
    fmt = "[%(asctime)s] %(levelname)s | %(message)s"
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(_ElapsedFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(console)
    if log_file:
        try:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(_ElapsedFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S"))
            logger.addHandler(fh)
        except Exception as e:  # pragma: no cover - defensive
            logger.warning(f"Failed to attach log file handler ({log_file}): {e}")
    logger.propagate = False
    return logger
