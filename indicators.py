import pandas as pd
import numpy as np


# ==================================
# EMA
# ==================================

def add_ema(df):

    df["EMA20"] = (
        df["Close"]
        .ewm(span=20, adjust=False)
        .mean()
    )

    df["EMA50"] = (
        df["Close"]
        .ewm(span=50, adjust=False)
        .mean()
    )

    df["EMA200"] = (
        df["Close"]
        .ewm(span=200, adjust=False)
        .mean()
    )

    return df


# ==================================
# RSI
# ==================================

def add_rsi(df, period=14):

    delta = df["Close"].diff()

    gain = delta.where(
        delta > 0,
        0
    )

    loss = -delta.where(
        delta < 0,
        0
    )

    avg_gain = (
        gain
        .rolling(period)
        .mean()
    )

    avg_loss = (
        loss
        .rolling(period)
        .mean()
    )

    rs = avg_gain / avg_loss

    df["RSI"] = (
        100 -
        (100 / (1 + rs))
    )

    return df


# ==================================
# MACD
# ==================================

def add_macd(df):

    ema12 = (
        df["Close"]
        .ewm(span=12, adjust=False)
        .mean()
    )

    ema26 = (
        df["Close"]
        .ewm(span=26, adjust=False)
        .mean()
    )

    df["MACD"] = ema12 - ema26

    df["MACD_SIGNAL"] = (
        df["MACD"]
        .ewm(span=9, adjust=False)
        .mean()
    )

    df["MACD_HIST"] = (
        df["MACD"] -
        df["MACD_SIGNAL"]
    )

    return df


# ==================================
# BOLLINGER BANDS
# ==================================

def add_bollinger(df):

    ma20 = (
        df["Close"]
        .rolling(20)
        .mean()
    )

    std20 = (
        df["Close"]
        .rolling(20)
        .std()
    )

    df["BB_MID"] = ma20

    df["BB_UPPER"] = (
        ma20 +
        (std20 * 2)
    )

    df["BB_LOWER"] = (
        ma20 -
        (std20 * 2)
    )

    return df


# ==================================
# STOCHASTIC
# ==================================

def add_stochastic(df):

    low14 = (
        df["Low"]
        .rolling(14)
        .min()
    )

    high14 = (
        df["High"]
        .rolling(14)
        .max()
    )

    df["STOCH_K"] = (
        (
            df["Close"] - low14
        ) /
        (
            high14 - low14
        )
    ) * 100

    df["STOCH_D"] = (
        df["STOCH_K"]
        .rolling(3)
        .mean()
    )

    return df


# ==================================
# ATR
# ==================================

def add_atr(df):

    high_low = (
        df["High"] -
        df["Low"]
    )

    high_close = np.abs(
        df["High"] -
        df["Close"].shift()
    )

    low_close = np.abs(
        df["Low"] -
        df["Close"].shift()
    )

    ranges = pd.concat(
        [
            high_low,
            high_close,
            low_close
        ],
        axis=1
    )

    true_range = (
        ranges.max(axis=1)
    )

    df["ATR"] = (
        true_range
        .rolling(14)
        .mean()
    )

    return df


# ==================================
# TREND ENGINE
# ==================================

def detect_trend(df):

    ema20 = float(
        df["EMA20"].iloc[-1]
    )

    ema50 = float(
        df["EMA50"].iloc[-1]
    )

    ema200 = float(
        df["EMA200"].iloc[-1]
    )

    if (
        ema20 > ema50 and
        ema50 > ema200
    ):
        return "Bullish"

    if (
        ema20 < ema50 and
        ema50 < ema200
    ):
        return "Bearish"

    return "Neutral"


# ==================================
# MASTER INDICATOR ENGINE
# ==================================

def apply_indicators(df):

    df = add_ema(df)

    df = add_rsi(df)

    df = add_macd(df)

    df = add_bollinger(df)

    df = add_stochastic(df)

    df = add_atr(df)

    return df
