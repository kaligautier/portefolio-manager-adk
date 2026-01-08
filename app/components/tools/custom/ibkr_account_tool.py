"""IBKR Account ID tool for retrieving the configured account ID."""

import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)


def get_my_account_id() -> str:
    """Get the configured IBKR account ID.

    This tool returns the IBKR account ID that is configured in the system.
    Use this tool when you need to identify which IBKR account to use for:
    - Placing orders via iserver_account_account_id_orders_post
    - Retrieving portfolio data
    - Checking account status
    - Any operation requiring an account ID

    The account ID is pre-configured in settings and does not require authentication.

    Returns:
        The IBKR account ID as a string (e.g., "DUO316496")

    Example:
        >>> account_id = get_my_account_id()
        >>> print(account_id)
        'DUO316496'
    """
    account_id = settings.IBKR_ACCOUNT_ID
    logger.info(f"Tool get_my_account_id called - returning account ID: {account_id}")
    return account_id
