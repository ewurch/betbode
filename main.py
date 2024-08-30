from scraper import scrape_matches
from arbitrage import calculate_arbitrage_roi
from telegram_bot import send_roi_message

def main():
    matches = scrape_matches()

    for match in matches:
        match['roi'] = calculate_arbitrage_roi(match['odds'])

    send_roi_message(matches)

if __name__ == '__main__':
    main()