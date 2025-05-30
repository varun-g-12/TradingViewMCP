import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Union

import pandas as pd
import requests
from mcp.server.fastmcp import FastMCP

from mcp_server.constants import COLUMNS, DATA, HEADERS, PARAMS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("Tradingview_mcp")

# Constants
TEMP_DIR = Path("tempDir")
API_URL = "https://scanner.tradingview.com/india/scan"
RECOMMENDATION_THRESHOLDS = {
    "strong_sell": (-1.0, -0.5),
    "sell": (-0.5, -0.1),
    "neutral": (-0.1, 0.1),
    "buy": (0.1, 0.5),
    "strong_buy": (0.5, 1.0),
}


class TradingDataError(Exception):
    """Custom exception for trading data operations."""

    pass


def setup_temp_directory() -> None:
    """Create temporary directory if it doesn't exist."""
    TEMP_DIR.mkdir(exist_ok=True)


def categorize_recommendation(value: float) -> str:
    """
    Categorize recommendation based on Recommend.All value.
    Args:
        value: The recommendation value to categorize
    Returns:
        The category string
    """
    if not isinstance(value, (int, float)) or pd.isna(value):  # type: ignore
        return "unknown"

    for category, (min_val, max_val) in RECOMMENDATION_THRESHOLDS.items():
        if min_val <= value <= max_val:
            return category

    return "unknown"


def fetch_trading_data(output_file: str) -> Path:
    """
    Fetch trading data from TradingView API and save to CSV.
    Args:
        output_file: Base name for the output file
    Returns:
        Path to the saved CSV file
    Raises:
        TradingDataError: If API request fails or data processing fails
    """
    try:
        logger.info("Fetching trading data from TradingView API")

        response = requests.post(
            API_URL, params=PARAMS, headers=HEADERS, data=json.dumps(DATA), timeout=30
        )
        response.raise_for_status()

        data = response.json()
        if not data or "data" not in data:
            raise TradingDataError("Invalid response format from API")

        api_data = data["data"]
        if not api_data:
            raise TradingDataError("No data returned from API")

        # Extract rows and create DataFrame
        rows = [row["d"] for row in api_data if "d" in row]
        if not rows:
            raise TradingDataError("No valid data rows found")

        df = pd.DataFrame(rows, columns=COLUMNS)

        # Add recommendation category
        df["recommendation_category"] = df["Recommend.All"].apply(  # type: ignore
            categorize_recommendation
        )

        # Save to CSV
        setup_temp_directory()
        output_path = TEMP_DIR / f"{output_file}.csv"
        df.to_csv(output_path, index=False)

        logger.info(f"Trading data saved to {output_path}")
        return output_path

    except requests.RequestException as e:
        raise TradingDataError(f"API request failed: {e}")
    except (KeyError, ValueError, pd.errors.ParserError) as e:
        raise TradingDataError(f"Data processing failed: {e}")
    except Exception as e:
        raise TradingDataError(f"Unexpected error: {e}")


def load_and_filter_stocks(csv_path: Path, tech_sig: str) -> List[Dict[str, Any]]:
    """
    Load CSV data and filter by technical signal.
    Args:
        csv_path: Path to the CSV file
        tech_sig: Technical signal to filter by
    Returns:
        List of filtered stock records
    Raises:
        TradingDataError: If file loading or filtering fails
    """
    try:
        if not csv_path.exists():
            raise TradingDataError(f"Data file not found: {csv_path}")

        df = pd.read_csv(csv_path)  # type: ignore

        if "recommendation_category" not in df.columns:
            raise TradingDataError("Missing recommendation_category column")

        filtered_df = df[df["recommendation_category"] == tech_sig]
        logger.info(f"Found {len(filtered_df)} stocks with {tech_sig} signal")

        return filtered_df.to_dict(orient="records")  # type: ignore

    except pd.errors.EmptyDataError:
        raise TradingDataError("CSV file is empty")
    except pd.errors.ParserError as e:
        raise TradingDataError(f"Failed to parse CSV: {e}")
    except Exception as e:
        raise TradingDataError(f"Failed to load and filter data: {e}")


@mcp.tool()
def get_stocks(
    tech_sig: Literal["buy", "strong_buy", "sell", "strong_sell", "neutral"],
) -> Union[List[Dict[str, Any]], str]:
    """
    Fetch stocks from TradingView scanner based on technical signal recommendation.

    Makes a POST request to TradingView's India scanner API to retrieve stock data,
    processes the response into a DataFrame, categorizes recommendations, and filters
    stocks based on the specified technical signal.

    Args:
        tech_sig: The technical signal category to filter by.
            Must be one of "buy", "strong_buy", "sell", "strong_sell", or "neutral".

    Returns:
        On success, returns a list of dictionaries containing stock data for stocks
        matching the specified technical signal. On failure, returns an error message string.
    """
    try:
        # Generate output filename with current date
        output_file = datetime.now().strftime("%Y-%m-%d")

        # Fetch and process trading data
        csv_path = fetch_trading_data(output_file)

        # Load and filter stocks
        stocks = load_and_filter_stocks(csv_path, tech_sig)

        if not stocks:
            return f"No stocks found with {tech_sig} signal for today"

        return stocks

    except TradingDataError as e:
        logger.error(f"Trading data error: {e}")
        return f"Unable to fetch stocks: {e}"
    except Exception as e:
        logger.error(f"Unexpected error in get_stocks: {e}")
        return f"Unable to fetch stocks due to unexpected error: {e}"


@mcp.tool()
def get_recommendation_summary() -> Union[Dict[str, int], str]:
    """
    Get a summary of recommendation counts for all categories.

    Returns:
        Dictionary with recommendation counts or error message.
    """
    try:
        output_file = datetime.now().strftime("%Y-%m-%d")
        csv_path = fetch_trading_data(output_file)

        df = pd.read_csv(csv_path)  # type: ignore
        summary = df["recommendation_category"].value_counts().to_dict()  # type: ignore

        return summary

    except Exception as e:
        logger.error(f"Error getting recommendation summary: {e}")
        return f"Unable to get recommendation summary: {e}"


if __name__ == "__main__":
    mcp.run()
