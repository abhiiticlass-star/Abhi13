import numpy as np


# ==========================================
# RECENT HIGH
# ==========================================

def recent_high(df, lookback=20):

    return float(
        df["High"]
        .tail(lookback)
        .max()
    )


# ==========================================
# RECENT LOW
# ==========================================

def recent_low(df, lookback=20):

    return float(
        df["Low"]
        .tail(lookback)
        .min()
    )


# ==========================================
# BREAKOUT UP
# ==========================================

def breakout_up(df):

    if len(df) < 25:
        return False

    current_close = float(
        df["Close"].iloc[-1]
    )

    resistance = float(
        df["High"]
        .iloc[-21:-1]
        .max()
    )

    return current_close > resistance


# ==========================================
# BREAKOUT DOWN
# ==========================================

def breakout_down(df):

    if len(df) < 25:
        return False

    current_close = float(
        df["Close"].iloc[-1]
    )

    support = float(
        df["Low"]
        .iloc[-21:-1]
        .min()
    )

    return current_close < support


# ==========================================
# MOMENTUM CHECK
# ==========================================

def momentum_strength(df):

    if len(df) < 10:
        return 0

    current = float(
        df["Close"].iloc[-1]
    )

    old = float(
        df["Close"].iloc[-6]
    )

    move = current - old

    return move


# ==========================================
# VOLUME CONFIRMATION
# ==========================================

def volume_confirmation(df):

    if "Volume" not in df.columns:
        return False

    try:

        current_volume = float(
            df["Volume"].iloc[-1]
        )

        avg_volume = float(
            df["Volume"]
            .tail(20)
            .mean()
        )

        return current_volume > avg_volume

    except:
        return False


# ==========================================
# FAKE BREAKOUT FILTER
# ==========================================

def fake_breakout(df):

    if len(df) < 3:
        return False

    last_close = float(
        df["Close"].iloc[-1]
    )

    prev_close = float(
        df["Close"].iloc[-2]
    )

    prev_high = float(
        df["High"].iloc[-2]
    )

    prev_low = float(
        df["Low"].iloc[-2]
    )

    if (
        last_close < prev_high and
        prev_close > prev_high
    ):
        return True

    if (
        last_close > prev_low and
        prev_close < prev_low
    ):
        return True

    return False


# ==========================================
# BREAKOUT DIRECTION
# ==========================================

def breakout_direction(df):

    if fake_breakout(df):
        return "NONE"

    if breakout_up(df):
        return "UP"

    if breakout_down(df):
        return "DOWN"

    return "NONE"


# ==========================================
# BREAKOUT SCORE
# ==========================================

def breakout_score(df):

    score = 0

    direction = breakout_direction(df)

    momentum = momentum_strength(df)

    if direction == "UP":
        score += 20

    if direction == "DOWN":
        score -= 20

    if momentum > 0:
        score += 10

    if momentum < 0:
        score -= 10

    if volume_confirmation(df):
        if direction == "UP":
            score += 10

        elif direction == "DOWN":
            score -= 10

    return score


# ==========================================
# BREAKOUT REPORT
# ==========================================

def breakout_analysis(df):

    return {

        "direction":
        breakout_direction(df),

        "momentum":
        round(
            momentum_strength(df),
            5
        ),

        "fake_breakout":
        fake_breakout(df),

        "volume_confirmed":
        volume_confirmation(df)
    }
