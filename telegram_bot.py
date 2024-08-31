from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio

from model import Odd, engine

from sqlalchemy.orm import Session

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print(TELEGRAM_BOT_TOKEN)
print(TELEGRAM_CHAT_ID)

def send_message(text):
    async def async_send_message():
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    
    asyncio.run(async_send_message())


MESSAGE_TEMPLATE = """
    📈 Arbitrage opportunities: 📈
"""

def send_roi_message(match: Odd):
    with Session(engine) as session:
        matches = session.query(Odd).filter(Odd.arbitrage_opportunity == True).all()
        message = str(MESSAGE_TEMPLATE)
        for match in matches:
            message += f"✅ {match.home_team} vs {match.away_team} - {match.roi*100:.2f}%\n"

    send_message(message)

