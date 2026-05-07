"""
utils/logger.py

Centralized logging utility for the automation framework.
Provides consistent logger formatting across modules.
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns configured logger instance.

    Args:
        name: Logger/module name.

    Returns:
        Configured logger object.
    """

    logger = logging.getLogger(name)

    if not logger.handlers:

        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger