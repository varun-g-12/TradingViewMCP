from pathlib import Path
from typing import Any, Dict, List

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

BASIC_INFO_COLUMNS: List[str] = [
    "name",
    "description",
    "logoid",
    "exchange",
    "market",
    "sector",
    "sector.tr",
    "currency",
    "fundamental_currency_code",
    "type",
    "typespecs",
    "update_mode",
    "pricescale",
    "minmov",
    "fractional",
    "minmove2",
]

PRICE_COLUMNS: List[str] = [
    "open",
    "high",
    "low",
    "close",
    "VWAP",
    "premarket_open",
    "premarket_high",
    "premarket_low",
    "premarket_close",
    "postmarket_open",
    "postmarket_high",
    "postmarket_low",
    "postmarket_close",
]

VOLUME_COLUMNS: List[str] = [
    "volume",
    "relative_volume_10d_calc",
    "relative_volume_10d_calc|1W",
    "average_volume_10d_calc",
    "average_volume_30d_calc",
]

FUNDAMENTAL_COLUMNS: List[str] = [
    "market_cap_basic",
    "price_earnings_ttm",
    "earnings_per_share_diluted_ttm",
    "earnings_per_share_diluted_yoy_growth_ttm",
    "dividends_yield_current",
]

TECHNICAL_COLUMNS: List[str] = [
    "SMA20",
    "SMA50",
    "SMA100",
    "EMA20",
    "EMA50",
    "EMA200",
    "RSI",
    "MACD.macd",
    "MACD.signal",
    "BB.upper",
    "BB.basis",
    "BB.lower",
    "ATR",
    "Pivot.M.Classic.R1",
    "Pivot.M.Classic.S1",
]

PERFORMANCE_COLUMNS: List[str] = [
    "change",
    "gap",
    "Perf.W",
    "Perf.1M",
    "Perf.3M",
    "beta_1_year",
]

CANDLESTICK_COLUMNS: List[str] = [
    "Candle.3BlackCrows",
    "Candle.3WhiteSoldiers",
    "Candle.AbandonedBaby.Bearish",
    "Candle.AbandonedBaby.Bullish",
    "Candle.Doji",
    "Candle.Doji.Dragonfly",
    "Candle.Doji.Gravestone",
    "Candle.Engulfing.Bearish",
    "Candle.Engulfing.Bullish",
    "Candle.EveningStar",
    "Candle.Hammer",
    "Candle.HangingMan",
    "Candle.Harami.Bearish",
    "Candle.Harami.Bullish",
    "Candle.InvertedHammer",
    "Candle.Kicking.Bearish",
    "Candle.Kicking.Bullish",
    "Candle.LongShadow.Lower",
    "Candle.LongShadow.Upper",
    "Candle.Marubozu.Black",
    "Candle.Marubozu.White",
    "Candle.MorningStar",
    "Candle.ShootingStar",
    "Candle.SpinningTop.Black",
    "Candle.SpinningTop.White",
    "Candle.TriStar.Bearish",
    "Candle.TriStar.Bullish",
]

RECOMMENDATION_COLUMNS: List[str] = [
    "recommendation_mark",
    "Recommend.All",
]

COLUMNS: List[str] = [
    "name",
    "description",
    "logoid",
    "update_mode",
    "type",
    "typespecs",
    "close",
    "pricescale",
    "minmov",
    "fractional",
    "minmove2",
    "currency",
    "change",
    "volume",
    "relative_volume_10d_calc",
    "market_cap_basic",
    "fundamental_currency_code",
    "price_earnings_ttm",
    "earnings_per_share_diluted_ttm",
    "earnings_per_share_diluted_yoy_growth_ttm",
    "dividends_yield_current",
    "sector.tr",
    "market",
    "sector",
    "recommendation_mark",
    "open",
    "high",
    "low",
    "VWAP",
    "premarket_open",
    "premarket_high",
    "premarket_low",
    "premarket_close",
    "postmarket_open",
    "postmarket_high",
    "postmarket_low",
    "postmarket_close",
    "SMA20",
    "SMA50",
    "SMA100",
    "EMA20",
    "EMA50",
    "EMA200",
    "RSI",
    "MACD.macd",
    "MACD.signal",
    "BB.upper",
    "BB.basis",
    "BB.lower",
    "ATR",
    "gap",
    "Pivot.M.Classic.R1",
    "Pivot.M.Classic.S1",
    "Perf.W",
    "Perf.1M",
    "Perf.3M",
    "beta_1_year",
    "relative_volume_10d_calc|1W",
    "average_volume_10d_calc",
    "average_volume_30d_calc",
    "Candle.3BlackCrows",
    "Candle.3WhiteSoldiers",
    "Candle.AbandonedBaby.Bearish",
    "Candle.AbandonedBaby.Bullish",
    "Candle.Doji",
    "Candle.Doji.Dragonfly",
    "Candle.Doji.Gravestone",
    "Candle.Engulfing.Bearish",
    "Candle.Engulfing.Bullish",
    "Candle.EveningStar",
    "Candle.Hammer",
    "Candle.HangingMan",
    "Candle.Harami.Bearish",
    "Candle.Harami.Bullish",
    "Candle.InvertedHammer",
    "Candle.Kicking.Bearish",
    "Candle.Kicking.Bullish",
    "Candle.LongShadow.Lower",
    "Candle.LongShadow.Upper",
    "Candle.Marubozu.Black",
    "Candle.Marubozu.White",
    "Candle.MorningStar",
    "Candle.ShootingStar",
    "Candle.SpinningTop.Black",
    "Candle.SpinningTop.White",
    "Candle.TriStar.Bearish",
    "Candle.TriStar.Bullish",
    "exchange",
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

RECOMMENDATION_THRESHOLDS: dict[str, Any] = {
    "strong_sell": (-1, -0.5),
    "sell": (-0.5, -0.1),
    "neutral": (-0.1, 0.1),
    "buy": (0.1, 0.5),
    "strong_buy": (0.5, 1),
}

API_URL: str = "https://scanner.tradingview.com/india/scan"

TEMP_DIR = Path("tempDir")
