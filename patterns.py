# ==========================================
# CANDLE PATTERN ENGINE
# ==========================================

def body_size(candle):

    return abs(
        float(candle["Close"]) -
        float(candle["Open"])
    )


def upper_wick(candle):

    return (
        float(candle["High"]) -
        max(
            float(candle["Open"]),
            float(candle["Close"])
        )
    )


def lower_wick(candle):

    return (
        min(
            float(candle["Open"]),
            float(candle["Close"])
        ) -
        float(candle["Low"])
    )


# ==========================================
# DOJI
# ==========================================

def is_doji(candle):

    body = body_size(candle)

    rng = (
        float(candle["High"]) -
        float(candle["Low"])
    )

    if rng == 0:
        return False

    return body <= (rng * 0.10)


# ==========================================
# HAMMER
# ==========================================

def is_hammer(candle):

    body = body_size(candle)

    low_wick = lower_wick(candle)

    up_wick = upper_wick(candle)

    return (
        low_wick > body * 2
        and
        up_wick < body
    )


# ==========================================
# SHOOTING STAR
# ==========================================

def is_shooting_star(candle):

    body = body_size(candle)

    low_wick = lower_wick(candle)

    up_wick = upper_wick(candle)

    return (
        up_wick > body * 2
        and
        low_wick < body
    )


# ==========================================
# BULLISH ENGULFING
# ==========================================

def bullish_engulfing(df):

    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return (

        float(prev["Close"])
        <
        float(prev["Open"])

        and

        float(curr["Close"])
        >
        float(curr["Open"])

        and

        float(curr["Open"])
        <
        float(prev["Close"])

        and

        float(curr["Close"])
        >
        float(prev["Open"])
    )


# ==========================================
# BEARISH ENGULFING
# ==========================================

def bearish_engulfing(df):

    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return (

        float(prev["Close"])
        >
        float(prev["Open"])

        and

        float(curr["Close"])
        <
        float(curr["Open"])

        and

        float(curr["Open"])
        >
        float(prev["Close"])

        and

        float(curr["Close"])
        <
        float(prev["Open"])
    )


# ==========================================
# MORNING STAR
# ==========================================

def morning_star(df):

    if len(df) < 3:
        return False

    a = df.iloc[-3]
    b = df.iloc[-2]
    c = df.iloc[-1]

    return (

        float(a["Close"])
        <
        float(a["Open"])

        and

        is_doji(b)

        and

        float(c["Close"])
        >
        float(c["Open"])
    )


# ==========================================
# EVENING STAR
# ==========================================

def evening_star(df):

    if len(df) < 3:
        return False

    a = df.iloc[-3]
    b = df.iloc[-2]
    c = df.iloc[-1]

    return (

        float(a["Close"])
        >
        float(a["Open"])

        and

        is_doji(b)

        and

        float(c["Close"])
        <
        float(c["Open"])
    )


# ==========================================
# CANDLE PSYCHOLOGY SCORE
# ==========================================

def psychology_score(df):

    score = 0

    last = df.iloc[-1]

    if bullish_engulfing(df):
        score += 20

    if bearish_engulfing(df):
        score -= 20

    if morning_star(df):
        score += 20

    if evening_star(df):
        score -= 20

    if is_hammer(last):
        score += 15

    if is_shooting_star(last):
        score -= 15

    if is_doji(last):
        score += 0

    return score


# ==========================================
# PATTERN DETECTOR
# ==========================================

def detect_pattern(df):

    last = df.iloc[-1]

    if bullish_engulfing(df):
        return "Bullish Engulfing"

    if bearish_engulfing(df):
        return "Bearish Engulfing"

    if morning_star(df):
        return "Morning Star"

    if evening_star(df):
        return "Evening Star"

    if is_hammer(last):
        return "Hammer"

    if is_shooting_star(last):
        return "Shooting Star"

    if is_doji(last):
        return "Doji"

    return "None"
