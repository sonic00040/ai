import sys
import os
import asyncio

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.services.supabase_service import SupabaseService
from app.services.rag_service import RAGService

# --- Configuration ---
COMPANY_NAME = "UrbanStep Footwear Ltd."
TELEGRAM_CHAT_ID = "-4884220020"
KNOWLEDGE_CONTENT = """The company is called UrbanStep Footwear Ltd. It was established in 2014 and has been operating for over 11 years. The headquarters is located in Accra, Ghana, with additional distribution centers in Lagos, Nigeria and London, UK.

UrbanStep specializes in athletic sneakers, casual footwear, formal leather shoes, sandals, and limited-edition collaborations. The company serves over 70,000 active customers worldwide and delivers to more than 45 countries.

Products are manufactured using premium leather, lightweight rubber soles, and eco-friendly materials. Each item goes through a triple-layer quality control process before leaving the warehouse.

Shipping timelines are 1–3 working days within Ghana and Nigeria, and 5–8 working days internationally. All orders come with a tracking number. Customers can also arrange in-store pickup at the Accra and Lagos branches.

Accepted payment methods include Visa, Mastercard, PayPal, Mobile Money, and bank transfers. Cash on delivery is available only for orders placed within Accra.

UrbanStep offers a 7-day return policy and a 3-month warranty against manufacturing defects. Customers can request size exchanges within the same timeframe.

Customer support is available 24/7 via WhatsApp, Telegram, and email. The official contact number is +233 550 123 456, and the support email is support@urbanstep.com.

The company operates an official website at www.urbanstep.com, where customers can browse catalogs, track orders, and access exclusive promotions."""

async def upload_knowledge():
    print("--- Uploading Knowledge for Existing Business ---")

    # Initialize services
    supabase_service = SupabaseService()
    rag_service = RAGService()

    # Get company details
    print(f"Checking for company with chat ID '{TELEGRAM_CHAT_ID}'...")
    company = supabase_service.get_company_by_telegram_chat_id(TELEGRAM_CHAT_ID)

    if company:
        company_id = company['id']
        print(f"Found company '{company['name']}' with ID: {company_id}")

        if KNOWLEDGE_CONTENT:
            print("\nGenerating embedding for the knowledge base...")
            embedding = rag_service.generate_embedding(KNOWLEDGE_CONTENT)
            
            print("Adding knowledge base entry to the database...")
            knowledge_entry = supabase_service.add_knowledge_base_entry(company_id, KNOWLEDGE_CONTENT, embedding)
            
            if knowledge_entry:
                print(f"\nSUCCESS: Knowledge base added successfully for {company['name']}.")
            else:
                print("ERROR: Failed to add knowledge base entry.")
        else:
            print("WARNING: No knowledge content provided. Nothing to upload.")
    else:
        print(f"ERROR: Could not find a company with Telegram Chat ID {TELEGRAM_CHAT_ID}. Please add the company first.")

if __name__ == "__main__":
    # Ensure .env is loaded for the script
    from dotenv import load_dotenv
    load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/.env')))
    
    # The service functions are synchronous, but we keep the async structure to be safe
    # In a real script, we might not need asyncio if all calls are sync.
    asyncio.run(upload_knowledge())
