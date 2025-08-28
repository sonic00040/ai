# Multi-Tenant AI Customer Response System

## Project Overview
This project aims to develop a scalable and customizable AI solution that enables businesses to automate customer interactions on messaging platforms, starting with Telegram. The system will dynamically adapt its responses based on the specific knowledge base provided by each registered business, leveraging Retrieval Augmented Generation (RAG) for intelligent, context-aware replies.

A core constraint for this project is a **$0 budget**, driving the use of open-source technologies and free-tier cloud services.

## Key Features (MVP 1 Focus)
*   **Dynamic AI Responses:** AI generates answers based on a business's unique knowledge base, not predefined FAQs.
*   **Multi-Tenancy:** Secure isolation of each business's data and AI models.
*   **Telegram Integration:** Full support for Telegram Bot API, with tenant identification via dedicated Telegram channels/groups.
*   **Cost-Effective:** Built entirely with open-source tools and free-tier services.

## Technology Stack
*   **Backend Language:** Python
*   **Web Framework:** FastAPI (for API endpoints and bot webhook)
*   **Database & Backend Services:** Supabase (PostgreSQL, Authentication, Storage)
*   **AI/NLP:** `sentence-transformers` (for embeddings), `scikit-learn`/`numpy` (for similarity search), and a small open-source LLM or free-tier LLM API for response generation.
*   **Messaging Integration:** `python-telegram-bot` library
*   **Future Admin UI (MVP 2):** React with Shadcn UI

## Project Structure
```
/multi-tenant-ai-bot/
|
|-- backend/
|   |-- app/
|   |   |-- __init__.py
|   |   |-- main.py             # Main application entry point (using FastAPI)
|   |   |-- bot/
|   |   |   |-- handler.py      # Logic for handling Telegram messages
|   |   |   |-- setup.py        # Logic for setting up the bot and its commands
|   |   |-- core/
|   |   |   |-- config.py       # Manages environment variables and settings
|   |   |-- services/
|   |   |   |-- rag_service.py    # Core RAG logic (embedding, searching)
|   |   |   |-- supabase_service.py # Handles all interactions with Supabase
|   |
|   |-- tests/                  # Directory for all tests
|   |-- .env.example            # Example file for environment variables
|   |-- requirements.txt        # List of Python dependencies
|   |-- Dockerfile              # To containerize the backend (future)
|
|-- frontend/                   # For the MVP 2 Admin UI (React & Shadcn)
|   |-- (empty for now)
|
|-- docs/
|   |-- prd.md                  # The Product Requirements Document
|   |-- architecture.md         # To document technical decisions
|
|-- scripts/
|   |-- add_business.py         # A utility script for adding new businesses to Supabase
|
|-- .gitignore                  # To specify files for Git to ignore
|-- README.md                   # Project overview, setup, and usage instructions
```

## Setup and Installation (Coming Soon)
Detailed instructions on setting up your development environment, configuring Supabase, and running the application will be provided here.

## How to Run (Coming Soon)
Instructions on how to start the bot and interact with it will be provided here.
