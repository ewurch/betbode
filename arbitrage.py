def calculate_arbitrage_roi(odds: list[float]):
    roi = 1 - sum(1 / odd for odd in odds)
    return roi
