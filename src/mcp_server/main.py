import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Literal, Union

import pandas as pd
import requests
from mcp.server.fastmcp import FastMCP

from mcp_server.constants import (
    API_URL,
    COLUMNS,
    DATA,
    HEADERS,
    PARAMS,
    RECOMMENDATION_THRESHOLDS,
    TECHNICAL_COLUMNS,
    TEMP_DIR,
    TECHNICAL_COLUMNS,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("Tradingview_mcp")
TEMP_FILE = TEMP_DIR / f"{datetime.datetime.now().date().strftime('%Y-%m-%d')}.csv"


class TradingViewError(Exception):
    """
    Custom exception class for TradingView-related errors.

    This exception is raised when there are issues with TradingView operations,
    such as API failures, authentication problems, or data retrieval errors.
    """

    pass


def categorize_recommendation(value: Union[float, int, Any]) -> str:
    """
    Categorize a numerical recommendation value into a predefined category.

    Args:
        value: The numerical value to categorize.

    Returns:
        The category name corresponding to the value's range, or "unknown"
        if the value cannot be categorized.
    """
    if not isinstance(value, (int, float)) or pd.isna(value):
        return "unknown"

    for category, (min_value, max_value) in RECOMMENDATION_THRESHOLDS.items():
        if min_value <= value <= max_value:
            return category

    return "unknown"


def _make_api_request() -> Dict[str, Any]:
    """
    Make API request to TradingView and return the response data.

    Returns:
        The API response data

    Raises:
        TradingViewError: If the API request fails
    """
    try:
        logger.info("Fetching data from TradingView API")
        response = requests.post(
            API_URL,
            params=PARAMS,
            data=json.dumps(DATA),
            headers=HEADERS,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise TradingViewError(f"API request failed: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response: {e}")
        raise TradingViewError(f"Invalid JSON response: {e}")


def _extract_data_rows(api_response: Dict[str, Any]) -> List[List[Any]]:
    """
    Extract data rows from API response.

    Args:
        api_response: The API response dictionary

    Returns:
        List of data rows

    Raises:
        TradingViewError: If data extraction fails
    """
    api_data = api_response.get("data")
    if not api_data:
        raise TradingViewError("Unable to find the 'data' key in API response")

    api_rows = [row.get("d") for row in api_data if row.get("d") is not None]
    if not api_rows:
        raise TradingViewError("Unable to find row data in API response")

    return api_rows


def _process_dataframe(api_rows: List[List[Any]]) -> pd.DataFrame:
    """
    Process raw API data into a pandas DataFrame.

    Args:
        api_rows: Raw data rows from API

    Returns:
        Processed DataFrame with recommendation categories
    """
    df = pd.DataFrame(api_rows, columns=COLUMNS)

    # Add recommendation category column
    df["recommendation_category"] = df["Recommend.All"].apply(categorize_recommendation)  # type: ignore

    return df


def _save_to_csv(df: pd.DataFrame, file_path: Path) -> None:
    """
    Save DataFrame to CSV file.

    Args:
        df: DataFrame to save
        file_path: Path to save the file
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")


def fetch_trading_view_data() -> None:
    """
    Fetch trading data from TradingView API and save it to a CSV file.

    Raises:
        TradingViewError: If any step in the process fails
    """
    try:
        # Make API request
        api_response = _make_api_request()

        # Extract data rows
        api_rows = _extract_data_rows(api_response)

        # Process into DataFrame
        df = _process_dataframe(api_rows)

        # Save to CSV
        _save_to_csv(df, TEMP_FILE)

    except TradingViewError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during data fetch: {e}")
        raise TradingViewError(f"Unexpected error during data fetch: {e}")


def _load_data() -> pd.DataFrame:
    """
    Load data from CSV file, fetching if necessary.

    Returns:
        DataFrame with trading data

    Raises:
        TradingViewError: If data loading fails
    """
    if not TEMP_FILE.exists():
        logger.info("Temporary file not found, fetching fresh data")
        fetch_trading_view_data()

    try:
        return pd.read_csv(TEMP_FILE)  # type: ignore
    except Exception as e:
        logger.error(f"Failed to load data from {TEMP_FILE}: {e}")
        raise TradingViewError(f"Failed to load data from file: {e}")


@mcp.tool()
def get_stock_by_category(
    category: Literal["strong_buy", "buy", "sell", "strong_sell", "neutral"],
) -> List[Dict[str, Any]]:
    """
    Get stocks filtered by recommendation category.

    Args:
        category: The recommendation category to filter by

    Returns:
        List of dictionaries containing stock information

    Raises:
        TradingViewError: If data loading or filtering fails
    """
    try:
        df = _load_data()

        filtered_df = df[df["recommendation_category"] == category]

        return filtered_df[["name", "recommendation_category"]].to_dict(  # type: ignore
            orient="records"
        )

    except Exception as e:
        logger.error(f"Failed to filter stocks by category {category}: {e}")
        raise TradingViewError(f"Failed to filter stocks by category: {e}")


@mcp.tool()
def get_technical_values(tickers: list[str]) -> dict[str, Any]:
    try:
        df = _load_data()
        df_filtered = df[df["name"].isin(tickers)][["name"] + TECHNICAL_COLUMNS]
        return df_filtered.to_dict("records")  # type: ignore
    except:
        logging.error(f"Failed to get technical values for {tickers}")
        raise TradingViewError(f"Failed to get technical values for {tickers}")


if __name__ == "__main__":
    mcp.run()
