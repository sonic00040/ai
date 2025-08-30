
import logging
import sys
import os
import asyncio
from telegram.ext import Application, MessageHandler, filters
from app.bot.handler import handle_message
from app.services.supabase_service import SupabaseService # Corrected import

# Enable logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.getLogger('telegram').setLevel(logging.DEBUG)

# Add a file handler to bot.log
file_handler = logging.FileHandler('bot.log', mode='w')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

async def run_bot_for_company(company_name: str, token: str):
    """Runs a single Telegram bot instance for a given company."""
    logger.info(f"Setting up bot for company: {company_name} with token {token[:10]}...")
    application = Application.builder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        await application.initialize()
        await application.updater.start_polling(poll_interval=1, timeout=30)
        logger.info(f"Bot for {company_name} started polling.")
        # Keep the bot running indefinitely
        await application.updater.idle()
    except Exception as e:
        logger.error(f"Error running bot for {company_name}: {e}")

async def main():
    logger.info("Bot script started. Initializing SupabaseService to fetch company tokens.")
    supabase_service = SupabaseService() # Instantiate the service

    # Fetch all companies with Telegram bot tokens
    companies = await supabase_service.get_all_companies()
    
    if not companies:
        logger.warning("No companies with Telegram bot tokens found in the database. No bots will be started.")
        return

    tasks = []
    for company in companies:
        company_name = company.get('name')
        telegram_bot_token = company.get('telegram_bot_token')
        
        if company_name and telegram_bot_token:
            tasks.append(run_bot_for_company(company_name, telegram_bot_token))
        else:
            logger.warning(f"Skipping company with missing name or token: {company}")

    logger.info(f"Starting {len(tasks)} bot instances...")
    await asyncio.gather(*tasks)
    logger.info("All bot instances are running.")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '.env')))
    asyncio.run(main())
