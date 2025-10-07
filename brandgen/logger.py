"""Logging utilities for the brandgen package."""

from __future__ import annotations
import logging
import sys
import time


_START_TIME = time.time()


class _ElapsedFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        elapsed = record.created - _START_TIME
        record.elapsed = f"{elapsed:8.2f}s"  # type: ignore[attr-defined]
        return super().format(record)


def configure_logger(name: str = "brandgen", level: int = logging.INFO) -> logging.Logger:
    """Configure and return a package logger with [timestamp] elapsed level message."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    fmt = "[%(asctime)s] %(levelname)s | %(message)s"
    handler.setFormatter(_ElapsedFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger
