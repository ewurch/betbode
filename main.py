from scraper import scrape_matches
from arbitrage import calculate_arbitrage_roi
from telegram_bot import send_roi_message
from model import Odd, engine
from sqlalchemy.orm import Session


def main():

    scrape_matches()
    with Session(engine) as session:
        matches = session.query(Odd).all()
        for match in matches:
            match.roi = calculate_arbitrage_roi([match.home_odds, match.draw_odds, match.away_odds])
            match.arbitrage_opportunity = match.roi > 0
            session.add(match)
        session.commit()

    send_roi_message(match)

if __name__ == '__main__':
    main()