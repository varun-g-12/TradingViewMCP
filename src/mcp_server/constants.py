from typing import Any, Dict, List, Literal

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
