"""IBKR Account ID tool for retrieving the configured account ID."""

import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)


def get_my_account_id() -> str:
    """
    Get the configured IBKR account ID.

    This tool returns the IBKR account ID that is configured in the system settings.
    Use this tool when you need to know which IBKR account to use for operations
    like placing orders, checking portfolio, or retrieving market data.

    Returns:
        str: The IBKR account ID (e.g., "DUO316496")
    """
    account_id = settings.IBKR_ACCOUNT_ID
    logger.info(f"Retrieved IBKR account ID: {account_id}")
    return account_id
