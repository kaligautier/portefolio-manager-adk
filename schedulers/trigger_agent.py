"""Function to trigger the portfolio master agent via API."""

import logging

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# API Configuration
API_BASE_URL = "http://localhost:8000"


def run_daily_analysis():
    """Run the daily portfolio analysis by calling the /run/daily endpoint."""
    logger.info("Triggering daily portfolio analysis via API...")

    try:
        url = f"{API_BASE_URL}/run/daily"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        result = response.json()
        logger.info("Daily analysis triggered: %s", result.get("message"))
        return result

    except requests.exceptions.RequestException as e:
        logger.error("Failed to trigger daily analysis: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise


if __name__ == "__main__":
    # Test the function
    run_daily_analysis()
