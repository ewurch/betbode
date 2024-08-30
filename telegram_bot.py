from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio

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

def send_roi_message(matches: list[dict]):
    message = ""
    for match in matches:
        if match['roi'] > 0:
            message += f"🔺 {match['match']} - {match['roi']}\n"  # Green triangle for positive ROI
        else:
            message += f"🔻 {match['match']} - No arbitrage opportunity\n"  # Red triangle for negative ROI

    send_message(message)

