# Architecture Design: Multi-Tenant AI Customer Response System

This document outlines the architectural decisions and technical flow for the Multi-Tenant AI Customer Response System, emphasizing its multi-tenancy, RAG implementation, and adherence to a $0 budget.

## 1. High-Level Architecture

```
+-----------------+
|   Telegram User |
+--------+--------+
         |
         | (Messages)
         v
+--------+--------+
| Telegram Bot API|
+--------+--------+
         |
         | (Webhook)
         v
+-----------------+
|   FastAPI Backend |
| (Python)        |
|   - Bot Handler   |
|   - RAG Service   |
|   - Supabase Svc  |
+--------+--------+
         |
         | (API Calls)
         v
+-----------------+
|    Supabase     |
| (PostgreSQL DB) |
|   - Companies   |
|   - Knowledge   |
+-----------------+
```

## 2. Multi-Tenancy Design

The system is designed from the ground up to support multiple independent businesses (tenants) with secure data isolation.

### Tenant Identification
Instead of explicit commands, tenant identification is based on the Telegram channel/group where the bot operates. Each dedicated Telegram channel/group will be linked to a specific company.

*   **Mechanism:**
    1.  A unique `telegram_chat_id` (from the Telegram channel/group) will be stored in the `companies` table in Supabase.
    2.  When a message is received, the `bot/handler.py` extracts the `telegram_chat_id`.
    3.  The `services/supabase_service.py` uses this `telegram_chat_id` to look up the corresponding `company_id`.
    4.  All subsequent data retrieval (e.g., knowledge base) is filtered by this `company_id`, ensuring strict tenant isolation.

### Database Schema (Supabase)

*   **`companies` table:**
    *   `id` (UUID, Primary Key)
    *   `name` (TEXT)
    *   `telegram_chat_id` (TEXT, Unique, Indexed) - Links to the Telegram channel/group.
    *   `created_at` (TIMESTAMP)
    *   ... (other company-specific metadata)

*   **`knowledge_bases` table:**
    *   `id` (UUID, Primary Key)
    *   `company_id` (UUID, Foreign Key to `companies.id`) - Crucial for isolation.
    *   `content` (TEXT) - The raw, unstructured knowledge text for the company.
    *   `embedding` (VECTOR) - Vector representation of the `content` for semantic search.
    *   `created_at` (TIMESTAMP)
    *   ... (other metadata like source, last updated)

## 3. Retrieval Augmented Generation (RAG) Workflow

The core of the AI's intelligence lies in its ability to dynamically generate responses from unstructured knowledge, rather than relying on predefined Q&A pairs.

1.  **User Query:** A user sends a message in a Telegram channel/group.
2.  **Telegram Bot Webhook:** The Telegram Bot API forwards the message to our FastAPI backend via a webhook.
3.  **Tenant Identification:** The `bot/handler.py` extracts the `telegram_chat_id` and uses `services/supabase_service.py` to retrieve the associated `company_id` and its knowledge base.
4.  **Knowledge Retrieval (`rag_service.py`):**
    *   The user's query is converted into an embedding using `sentence-transformers`.
    *   This query embedding is used to perform a semantic similarity search against the `embedding` column in the `knowledge_bases` table (filtered by `company_id`).
    *   The most relevant `content` snippets (paragraphs, sentences) from the company's knowledge base are retrieved.
5.  **Response Generation (`rag_service.py`):**
    *   The retrieved relevant content, along with the original user query, is sent to a Large Language Model (LLM).
    *   The LLM synthesizes this information into a coherent, natural language response.
6.  **Response to User:** The generated response is sent back to the user via the Telegram Bot API.

## 4. Technology Choices Justification

*   **Python:** Excellent for AI/NLP tasks, vast ecosystem of libraries.
*   **FastAPI:** High-performance web framework for building APIs, ideal for handling Telegram webhooks. Provides automatic API documentation.
*   **Supabase:** Open-source Firebase alternative providing PostgreSQL database, authentication, and real-time capabilities. Its generous free tier and vector database support (for embeddings) make it perfect for the $0 budget.
*   **`python-telegram-bot`:** A robust and well-maintained library for interacting with the Telegram Bot API.
*   **`sentence-transformers`:** Efficient library for generating high-quality text embeddings, crucial for semantic search in RAG.
*   **Open-source LLM / Free-tier LLM API:** Adheres to the $0 budget. Requires careful token management and optimization.
*   **React & Shadcn UI (for MVP 2 Admin UI):** Modern, component-based frontend framework and UI library for building a clean, maintainable, and user-friendly admin dashboard.

## 5. Scalability Considerations

*   **Database:** PostgreSQL (via Supabase) is highly scalable. Proper indexing and query optimization will be key.
*   **Backend:** FastAPI applications can be scaled horizontally by running multiple instances. Containerization with Docker will facilitate this
*   **LLM:** The choice of LLM and its hosting will be the primary scaling bottleneck. Starting with a small, self-hosted model or a free-tier API will require careful monitoring and potential future upgrades if usage grows beyond free limits.
*   **Multi-tenancy:** The design ensures that adding new tenants primarily involves adding data, not re-architecting the application.
