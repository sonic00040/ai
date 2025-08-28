import sys
import os
import asyncio
from uuid import uuid4

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.core.config import settings
from app.services.supabase_service import SupabaseService
from app.services.rag_service import RAGService

async def add_business():
    print("--- Add New Business ---")

    # Initialize services
    supabase_service = SupabaseService()
    rag_service = RAGService()

    # Get company details
    company_name = input("Enter Company Name: ")
    telegram_bot_token = input("Enter Telegram Bot Token: ")

    # Add company to Supabase
    print(f"\nAdding company '{company_name}' with bot token '{telegram_bot_token[:10]}...'")
    company = supabase_service.add_company(company_name, telegram_bot_token)

    if company:
        company_id = company['id']
        print(f"Company '{company_name}' added successfully with ID: {company_id}")
        print("\n--- Enter Knowledge Base Content ---")
        print("Type 'END_KNOWLEDGE' on a new line to finish.")

        knowledge_content_lines = []
        while True:
            line = input()
            if line == "END_KNOWLEDGE":
                break
            knowledge_content_lines.append(line)
        
        knowledge_content = "\n".join(knowledge_content_lines).strip()

        if knowledge_content:
            print("\nGenerating embedding for knowledge base...")
            embedding = rag_service.generate_embedding(knowledge_content)
            
            print("Adding knowledge base entry...")
            knowledge_entry = supabase_service.add_knowledge_base_entry(company_id, knowledge_content, embedding)
            
            if knowledge_entry:
                print(f"Knowledge base added successfully for {company_name}.")
            else:
                print("Failed to add knowledge base entry.")
        else:
            print("No knowledge content provided. Skipping knowledge base entry.")
    else:
        print("Failed to add company. It might already exist or there was a database error.")

if __name__ == "__main__":
    # Ensure .env is loaded for the script
    from dotenv import load_dotenv
    load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/.env')))
    
    asyncio.run(add_business())
