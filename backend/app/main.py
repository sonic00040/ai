import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

from app.core.config import settings
from app.bot.handler import handle_message
from app.services.supabase_service import supabase_service

# --- Configure Logging ---
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# File handler
file_handler = logging.FileHandler("bot.log")
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)
# --- End Logging Configuration ---

# Dictionary to hold all our bot Application instances, keyed by token
bot_apps: Dict[str, Application] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for the FastAPI application.
    On startup, it initializes all bots from the database and sets their webhooks.
    """
    # --- Startup ---
    logger.info("Starting up...")
    
    bot_tokens = supabase_service.get_all_bot_tokens()
    
    if not bot_tokens:
        logger.warning("No bot tokens found in the database. No bots will be started.")
    
    for token in bot_tokens:
        application = Application.builder().token(token).build()
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        webhook_url = f"{settings.WEBHOOK_DOMAIN}/webhook/{token}"
        
        try:
            await application.initialize()
            await application.bot.set_webhook(url=webhook_url)
            logger.info(f"Webhook set for bot {token[:10]}... at {webhook_url}")
            bot_apps[token] = application
        except Exception as e:
            logger.error(f"Failed to initialize bot {token[:10]}...: {e}")

    yield

    # --- Shutdown ---
    logger.info("Shutting down...")
    for token, application in bot_apps.items():
        try:
            if application.running:
                await application.bot.delete_webhook()
                logger.info(f"Webhook deleted for bot {token[:10]}... ")
                await application.shutdown()
        except Exception as e:
            logger.error(f"Failed to shutdown bot {token[:10]}...: {e}")
    
    logger.info("All bots have been shut down.")


# Create the FastAPI app with the lifespan manager
app = FastAPI(lifespan=lifespan)

@app.post("/webhook/{token}")
async def handle_webhook(token: str, request: Request):
    """
    This single endpoint receives updates from all Telegram bots.
    """
    application = bot_apps.get(token)
    if not application:
        logger.error(f"Update received for an unknown bot token: {token}")
        raise HTTPException(status_code=404, detail="Bot not found")

    try:
        update_data = await request.json()
        update = Update.de_json(update_data, application.bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing update for bot {token[:10]}...: {e}")
        return {"status": "error"}


@app.get("/")
async def read_root():
    """Root endpoint to check if the backend is running."""
    return {"message": "Multi-Tenant AI Bot Backend is running!"}
