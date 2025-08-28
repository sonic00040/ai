import sys
import os
import asyncio
from datetime import datetime, timedelta, timezone
import logging # Import logging

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.services.supabase_service import SupabaseService

# Configure logging for the script
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # Get a logger for this script

async def setup_test_subscription():
    logger.info("--- Setting up Test Subscription ---") # Use logger.info

    supabase_service = SupabaseService()

    # 1. Define and create the "Basic" plan if it doesn't exist
    plan_name = "Basic"
    plan_price = 10.00
    plan_token_limit = 1050000  # From our plans.md

    logger.info(f"Checking for '{plan_name}' plan...") # Use logger.info
    plan = supabase_service.get_plan_by_name(plan_name)

    if not plan:
        logger.info(f"'{plan_name}' plan not found. Creating it...") # Use logger.info
        plan = supabase_service.add_plan(plan_name, plan_price, plan_token_limit)
        if not plan:
            logger.error("Error: Could not create the plan. Exiting.") # Use logger.error
            return
        logger.info(f"'{plan_name}' plan created successfully.") # Use logger.info
    else:
        logger.info(f"'{plan_name}' plan already exists.") # Use logger.info

    plan_id = plan['id']

    # 2. Get the test company
    company_name = "UrbanStep Footwear Ltd."
    logger.info(f"Fetching company '{company_name}'...") # Use logger.info
    company = supabase_service.get_company_by_name(company_name)

    if not company:
        logger.error(f"Error: Company '{company_name}' not found. Please add it first using add_business.py. Exiting.") # Use logger.error
        return
    
    company_id = company['id']
    logger.info(f"Found company with ID: {company_id}") # Use logger.info

    # 3. Check if the company already has an active subscription
    logger.info("Checking for existing active subscription...") # Use logger.info
    active_subscription = supabase_service.get_active_subscription_by_company_id(company_id)

    if active_subscription:
        logger.info("Company already has an active subscription. Setup is complete.") # Use logger.info
        return

    # 4. Create a new subscription for the company
    logger.info("No active subscription found. Creating a new one for the 'Basic' plan...") # Use logger.info
    now = datetime.now(timezone.utc)
    start_date = now.isoformat()
    end_date = (now + timedelta(days=30)).isoformat()

    new_subscription = supabase_service.add_subscription(company_id, plan_id, start_date, end_date)

    if new_subscription:
        logger.info("Successfully subscribed company to the 'Basic' plan.") # Use logger.info
    else:
        logger.error("Error: Failed to create the subscription.") # Use logger.error

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/.env')))
    
    # Supabase client requires an async context
    # The script itself doesn't use await, but the underlying library might.
    # Running it with asyncio.run is safer.
    asyncio.run(setup_test_subscription())