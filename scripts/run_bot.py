import asyncio
import logging
import sys
import os
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.bot.setup import setup_bot_application
from app.bot.handler import handle_message
from telegram.ext import MessageHandler, filters

# Enable logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.getLogger('telegram').setLevel(logging.DEBUG)

# Add a file handler to log to bot.log
file_handler = logging.FileHandler('bot.log', mode='w')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

def send_heartbeat(context):
    logger.info(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Bot is running and waiting for messages...")

def main():
    logger.info("Bot script started.")
    logger.info("Setting up bot application...")
    application = setup_bot_application()
    application.http_version = "1.1"
    application.local_address = "0.0.0.0"
    logger.info("Bot application setup complete.")

    logger.info("Adding message handler...")
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Message handler added.")

    logger.info("Starting polling...")
    application.start_polling(poll_interval=1, timeout=30)
    application.idle()

if __name__ == "__main__":
    main()
