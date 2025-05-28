import json
from typing import Any, Dict, List, Literal

import pandas as pd
import requests
from mcp.server.fastmcp import FastMCP

HEADERS: Dict[str, str] = {
    "accept": "application/json",
    "accept-language": "en-IN,en-GB;q=0.9,en;q=0.8,en-US;q=0.7",
    "content-type": "text/plain;charset=UTF-8",
    "origin": "https://in.tradingview.com",
    "referer": "https://in.tradingview.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
}

PARAMS: Dict[str, str] = {
    "label-product": "screener-stock",
}

COLUMNS: List[str] = [
    "name",
    "close",
    "change",
    "volume",
    "relative_volume_10d_calc",
    "Recommend.All",
]

SYMBOLS: List[str] = ["SYML:NSE;NIFTY", "SYML:NSE;NIFTYJR"]

MARKETS: List[str] = ["india"]

DATA: Dict[str, Any] = {
    "columns": COLUMNS,
    "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
    "symbols": {"symbolset": SYMBOLS},
    "markets": MARKETS,
}

# Create an MCP server
mcp = FastMCP("Tradingview_mcp")


def categorize_recommendation(value: float) -> str:
    """Categorize recommendation based on Recommend.All value."""
    if -0.1 <= value <= 0.1:
        return "neutral"
    elif 0.1 < value <= 0.5:
        return "buy"
    elif 0.5 < value <= 1:
        return "strong_buy"
    elif -0.5 <= value < -0.1:
        return "sell"
    elif -1 <= value < -0.5:
        return "strong_sell"
    else:
        return "unknown"


# Retrieve stocks that have buy or strong buy signals based on technical indicators
@mcp.tool()
def get_stocks(
    tech_sig: Literal["buy", "strong_buy", "sell", "strong_sell"],
) -> str | Dict[str, Any]:
    """
    Fetch stocks from TradingView scanner based on technical signal recommendation.

    Makes a POST request to TradingView's India scanner API to retrieve stock data,
    processes the response into a DataFrame, categorizes recommendations, and filters
    stocks based on the specified technical signal.

    Args:
        tech_sig (Literal["buy", "strong_buy", "sell", "strong_sell"]): The technical signal category to filter by.
            Must be either of "buy", "strong_buy", "sell" or "strong_sell".

    Returns:
        str | Dict[str, Any]: On success, returns a list of dictionaries containing
            stock data for stocks matching the specified technical signal. On failure,
            returns an error message string.

    Raises:
        The function catches all exceptions and returns them as error message strings
        rather than raising them.
    """
    try:
        response = requests.post(
            "https://scanner.tradingview.com/india/scan",
            params=PARAMS,
            headers=HEADERS,
            data=json.dumps(DATA),
        )
        response.raise_for_status()
        data = response.json().get("data")
        rows = [row["d"] for row in data]
        df = pd.DataFrame(rows, columns=COLUMNS)
        df["recommendation_category"] = df["Recommend.All"].apply(  # type: ignore
            categorize_recommendation
        )
        return df[df["recommendation_category"] == tech_sig].to_dict(orient="records")  # type: ignore
    except Exception as e:
        return f"Unable to fetch the stocks due to error: {e}"


if __name__ == "__main__":
    mcp.run()
