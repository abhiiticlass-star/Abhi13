import yfinance as yf
from datetime import datetime

from indicators import (
    apply_indicators,
    detect_trend
)

from patterns import (
    detect_pattern,
    psychology_score
)

from support_resistance import (
    sr_score,
    sr_analysis
)

from breakout import (
    breakout_score,
    breakout_analysis
)


# ==========================================
# MARKET STATUS
# ==========================================

def market_open():

    day = datetime.utcnow().weekday()

    # Saturday=5 Sunday=6

    if day in [5, 6]:
        return False

    return True


# ==========================================
# DOWNLOAD DATA
# ==========================================

def get_data(pair, timeframe):

    interval = "1m"

    if str(timeframe) == "5":
        interval = "5m"

    try:

        df = yf.download(
            tickers=pair,
            interval=interval,
            period="2d",
            progress=False,
            auto_adjust=True
        )

        if df is None:
            return None

        if len(df) < 100:
            return None

        return df

    except:
        return None


# ==========================================
# TREND SCORE
# ==========================================

def trend_score(df):

    trend = detect_trend(df)

    if trend == "Bullish":
        return 20

    if trend == "Bearish":
        return -20

    return 0


# ==========================================
# RSI SCORE
# ==========================================

def rsi_score(df):

    try:

        rsi = float(
            df["RSI"].iloc[-1]
        )

        if rsi < 30:
            return 15

        if rsi > 70:
            return -15

        return 0

    except:
        return 0


# ==========================================
# MACD SCORE
# ==========================================

def macd_score(df):

    try:

        macd = float(
            df["MACD"].iloc[-1]
        )

        signal = float(
            df["MACD_SIGNAL"].iloc[-1]
        )

        if macd > signal:
            return 10

        if macd < signal:
            return -10

        return 0

    except:
        return 0


# ==========================================
# BOLLINGER SCORE
# ==========================================

def bollinger_score(df):

    try:

        close = float(
            df["Close"].iloc[-1]
        )

        upper = float(
            df["BB_UPPER"].iloc[-1]
        )

        lower = float(
            df["BB_LOWER"].iloc[-1]
        )

        if close <= lower:
            return 10

        if close >= upper:
            return -10

        return 0

    except:
        return 0


# ==========================================
# TOTAL SCORE
# ==========================================

def total_score(df):

    score = 50

    score += trend_score(df)

    score += rsi_score(df)

    score += macd_score(df)

    score += bollinger_score(df)

    score += psychology_score(df)

    score += sr_score(df)

    score += breakout_score(df)

    score = max(0, min(100, score))

    return int(score)


# ==========================================
# M5 TREND
# ==========================================

def get_m5_trend(pair):

    try:

        m5 = yf.download(
            tickers=pair,
            interval="5m",
            period="2d",
            progress=False,
            auto_adjust=True
        )

        if len(m5) < 100:
            return "Neutral"

        m5 = apply_indicators(m5)

        return detect_trend(m5)

    except:
        return "Neutral"


# ==========================================
# SIGNAL DECISION
# ==========================================

def decide_signal(score):

    if score >= 75:
        return "CALL"

    if score <= 25:
        return "PUT"

    return "AVOID"


# ==========================================
# MAIN ENGINE
# ==========================================

def generate_signal(pair, timeframe):

    if not market_open():

        return {

            "pair":
            pair.replace("=X", ""),

            "signal":
            "MARKET CLOSED",

            "score":
            0,

            "trend":
            "Closed",

            "trendM5":
            "Closed",

            "market":
            "closed"
        }

    df = get_data(
        pair,
        timeframe
    )

    if df is None:

        return {

            "pair":
            pair.replace("=X", ""),

            "signal":
            "AVOID",

            "score":
            50,

            "trend":
            "Neutral",

            "trendM5":
            "Neutral",

            "market":
            "open"
        }

    df = apply_indicators(df)

    trend = detect_trend(df)

    trend_m5 = get_m5_trend(pair)

    score = total_score(df)

    signal = decide_signal(score)

    pattern = detect_pattern(df)

    sr_data = sr_analysis(df)

    breakout_data = breakout_analysis(df)

    return {

        "pair":
        pair.replace("=X", ""),

        "signal":
        signal,

        "score":
        score,

        "trend":
        trend,

        "trendM5":
        trend_m5,

        "market":
        "open",

        "time":
        datetime.utcnow().strftime("%H:%M:%S"),

        "timeframe":
        f"M{timeframe}",

        "pattern":
        pattern,

        "support":
        sr_data["support"],

        "resistance":
        sr_data["resistance"],

        "breakout":
        breakout_data["direction"],

        "fake_breakout":
        breakout_data["fake_breakout"],

        "momentum":
        breakout_data["momentum"]
  }
