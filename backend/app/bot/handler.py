import logging
import time
from telegram import Update
from telegram.ext import ContextTypes
from app.services.supabase_service import supabase_service
from app.services.rag_service import rag_service
from app.services.usage_service import usage_service

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming text messages, identifies tenant, and generates response."""
    start_time = time.time()
    if update.message and update.message.text:
        user_query = update.message.text
        bot_token = context.bot.token
        chat_id = str(update.message.chat_id)

        logger.info(f"Received message from chat_id {chat_id} on bot {bot_token[:10]}...")

        # 1. Identify Tenant
        company = supabase_service.get_company_by_telegram_bot_token(bot_token)
        if not company:
            await update.message.reply_text("This bot is not registered with any company. Please contact the administrator.")
            logger.warning(f"Unregistered bot_token: {bot_token}")
            return

        company_id = company['id']
        company_name = company['name']
        logger.info(f"Message for company: {company_name} (ID: {company_id})")

        # 2. Check for Active Subscription
        subscription = supabase_service.get_active_subscription_by_company_id(company_id)
        if not subscription:
            await update.message.reply_text("This company does not have an active subscription. Please contact the administrator.")
            logger.warning(f"No active subscription for company ID: {company_id}")
            return

        # 3. Enforce Usage Limits
        if usage_service.has_exceeded_limit(subscription):
            await update.message.reply_text("You have exceeded your monthly token limit. Please upgrade your plan or wait for the next billing cycle.")
            logger.warning(f"Token limit exceeded for company ID: {company_id}")
            return

        # 4. Retrieve Knowledge Base
        knowledge_bases = supabase_service.get_knowledge_bases_by_company_id(company_id)
        if not knowledge_bases:
            await update.message.reply_text(f"No knowledge base found for {company_name}. Please contact the administrator to upload knowledge.")
            logger.warning(f"No knowledge base for company ID: {company_id}")
            return

        # 5. Generate Query Embedding
        query_embedding = rag_service.generate_embedding(user_query)

        # 6. Semantic Search
        relevant_knowledge = rag_service.semantic_search(query_embedding, knowledge_bases)

        # 7. Generate Response with LLM
        ai_response, token_count = rag_service.generate_response_with_llm(user_query, relevant_knowledge)

        # 8. Record Usage
        if token_count > 0:
            usage_service.record_usage(subscription_id=subscription['id'], total_tokens=token_count)

        await update.message.reply_text(ai_response)
        end_time = time.time()
        logger.info(f"Total processing time: {end_time - start_time:.4f} seconds")
        logger.info(f"Replied to chat_id {chat_id} for company {company_name}.")
    else:
        logger.info(f"Received non-text message or empty message from {update.message.chat_id}")
        await update.message.reply_text("I can only process text messages at the moment.")
