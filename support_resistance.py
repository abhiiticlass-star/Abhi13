import numpy as np


# ==========================================
# BASIC SUPPORT
# ==========================================

def get_support(df, lookback=30):

    lows = df["Low"].tail(lookback)

    return float(lows.min())


# ==========================================
# BASIC RESISTANCE
# ==========================================

def get_resistance(df, lookback=30):

    highs = df["High"].tail(lookback)

    return float(highs.max())


# ==========================================
# DYNAMIC SUPPORT ZONE
# ==========================================

def support_zone(df, lookback=30):

    support = get_support(df, lookback)

    zone_size = support * 0.001

    return {
        "low": support - zone_size,
        "high": support + zone_size
    }


# ==========================================
# DYNAMIC RESISTANCE ZONE
# ==========================================

def resistance_zone(df, lookback=30):

    resistance = get_resistance(df, lookback)

    zone_size = resistance * 0.001

    return {
        "low": resistance - zone_size,
        "high": resistance + zone_size
    }


# ==========================================
# SUPPORT BOUNCE
# ==========================================

def support_bounce(df):

    close = float(df["Close"].iloc[-1])

    zone = support_zone(df)

    return (
        zone["low"]
        <= close
        <= zone["high"]
    )


# ==========================================
# RESISTANCE REJECTION
# ==========================================

def resistance_rejection(df):

    close = float(df["Close"].iloc[-1])

    zone = resistance_zone(df)

    return (
        zone["low"]
        <= close
        <= zone["high"]
    )


# ==========================================
# ZONE STRENGTH
# ==========================================

def zone_strength(df):

    support = get_support(df)

    resistance = get_resistance(df)

    closes = df["Close"].tail(50)

    support_hits = 0
    resistance_hits = 0

    for price in closes:

        if abs(price - support) < support * 0.002:
            support_hits += 1

        if abs(price - resistance) < resistance * 0.002:
            resistance_hits += 1

    return {
        "support_hits": support_hits,
        "resistance_hits": resistance_hits
    }


# ==========================================
# STRONG SUPPORT?
# ==========================================

def strong_support(df):

    strength = zone_strength(df)

    return strength["support_hits"] >= 3


# ==========================================
# STRONG RESISTANCE?
# ==========================================

def strong_resistance(df):

    strength = zone_strength(df)

    return strength["resistance_hits"] >= 3


# ==========================================
# REJECTION DETECTION
# ==========================================

def bullish_rejection(df):

    last = df.iloc[-1]

    body = abs(
        float(last["Close"]) -
        float(last["Open"])
    )

    lower_wick = (
        min(
            float(last["Open"]),
            float(last["Close"])
        )
        -
        float(last["Low"])
    )

    return lower_wick > (body * 2)


def bearish_rejection(df):

    last = df.iloc[-1]

    body = abs(
        float(last["Close"]) -
        float(last["Open"])
    )

    upper_wick = (
        float(last["High"])
        -
        max(
            float(last["Open"]),
            float(last["Close"])
        )
    )

    return upper_wick > (body * 2)


# ==========================================
# SUPPORT RESISTANCE SCORE
# ==========================================

def sr_score(df):

    score = 0

    if support_bounce(df):
        score += 15

    if resistance_rejection(df):
        score -= 15

    if bullish_rejection(df):
        score += 10

    if bearish_rejection(df):
        score -= 10

    if strong_support(df):
        score += 10

    if strong_resistance(df):
        score -= 10

    return score


# ==========================================
# ANALYSIS PANEL DATA
# ==========================================

def sr_analysis(df):

    return {

        "support":
        round(get_support(df), 5),

        "resistance":
        round(get_resistance(df), 5),

        "support_zone":
        support_zone(df),

        "resistance_zone":
        resistance_zone(df),

        "support_strength":
        zone_strength(df)["support_hits"],

        "resistance_strength":
        zone_strength(df)["resistance_hits"]
    }
