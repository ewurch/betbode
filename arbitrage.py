def calculate_arbitrage_roi(odds: dict[str, float]):
    roi = 1 - sum(1 / odd for odd in odds.values())
    return roi
