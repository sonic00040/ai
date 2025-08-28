### Project Roadmap: Multi-Tenant AI Customer Response System

**Goal:** To deliver a fully functional, secure, and scalable multi-tenant AI customer response system, starting with a Telegram bot, adhering to a $0 budget.

---

### **Plan 1: Core MVP - Telegram Bot with Basic RAG & Multi-Tenancy**

**Objective:** To establish the fundamental multi-tenant AI bot on Telegram, demonstrating dynamic responses from company-specific knowledge bases. This is the absolute minimum viable product.

**Deliverables:**
*   Functional Telegram bot responding to user queries.
*   Ability to add new companies and their knowledge bases (via script).
*   Basic RAG working with semantic search.
*   Secure tenant isolation at the database level.

**Steps:**

1.  **Project Setup & Environment (Backend)**
    *   Create the project directory structure (`multi-tenant-ai-bot/backend/`, `docs/`, `scripts/`).
    *   Initialize Python virtual environment.
    *   Create `requirements.txt` with core dependencies: `fastapi`, `uvicorn`, `python-telegram-bot`, `supabase-py`, `sentence-transformers`, `psycopg2-binary` (for Supabase).
    *   Create `.env.example` for environment variables (Telegram Bot Token, Supabase URL, Supabase Key).
    *   Set up `.gitignore`.

2.  **Supabase Project & Initial Schema**
    *   Create a new project in Supabase.
    *   Enable the `pg_vector` extension in your Supabase database.
    *   Define the `public.companies` table:
        *   `id` (UUID, Primary Key, default `gen_random_uuid()`)
        *   `name` (TEXT, NOT NULL)
        *   `telegram_chat_id` (TEXT, UNIQUE, NOT NULL)
        *   `created_at` (TIMESTAMP WITH TIME ZONE, default `now()`)
    *   Define the `public.knowledge_bases` table:
        *   `id` (UUID, Primary Key, default `gen_random_uuid()`)
        *   `company_id` (UUID, Foreign Key to `public.companies.id`, NOT NULL)
        *   `content` (TEXT, NOT NULL)
        *   `embedding` (VECTOR(768), NOT NULL) - *Assuming a 768-dimension model like `all-MiniLM-L6-v2`.*
        *   `created_at` (TIMESTAMP WITH TIME ZONE, default `now()`)
    *   Implement initial **Row-Level Security (RLS)** policies for `public.companies` and `public.knowledge_bases` to ensure basic read/write access for the service role and prevent public access. (Refine later in Plan 2).

3.  **Backend Core Development (FastAPI & Supabase Integration)**
    *   Implement `backend/app/core/config.py` to load environment variables securely.
    *   Implement `backend/app/services/supabase_service.py`:
        *   Initialize Supabase client.
        *   Functions for basic CRUD on `companies` and `knowledge_bases`.
        *   Function to fetch `company_id` by `telegram_chat_id`.
        *   Function to insert/retrieve knowledge base entries.
    *   Implement `backend/app/services/rag_service.py`:
        *   Function to load `sentence-transformers` model.
        *   Function to generate embeddings for text.
        *   Function for semantic search (cosine similarity) within a given set of knowledge embeddings.
        *   Placeholder for LLM integration (e.g., simple text concatenation or a very basic local model).

4.  **Telegram Bot Integration**
    *   Create a new Telegram bot via BotFather and obtain its token.
    *   Implement `backend/app/bot/setup.py` to set up the Telegram webhook (FastAPI endpoint).
    *   Implement `backend/app/bot/handler.py`:
        *   Receive incoming Telegram messages.
        *   Extract `telegram_chat_id`.
        *   Use `supabase_service` to identify the `company_id`.
        *   Pass user query and company-specific knowledge to `rag_service`.
        *   Send generated response back to Telegram.

5.  **Initial RAG Implementation & Scripting**
    *   Integrate the `rag_service` into the `bot/handler` to perform retrieval and initial response generation.
    *   Create `scripts/add_business.py`: A simple Python script to manually add a new company to `public.companies` and upload its initial knowledge base to `public.knowledge_bases` (including embedding generation).

6.  **Testing & Initial Deployment**
    *   Manually test the bot by adding a test company and interacting with it in a Telegram channel.
    *   Deploy the FastAPI backend to a free-tier cloud VM (e.g., Google Cloud f1-micro).

---

### **Plan 2: Enhanced Features & Admin UI (MVP 2)**

**Objective:** To improve the usability for managing businesses and knowledge bases, and to enhance the AI's capabilities and data logging.

**Deliverables:**
*   Basic web-based Admin UI for managing companies and knowledge.
*   Comprehensive RLS for all tables.
*   Conversation history logging.
*   Potentially more advanced RAG.

**Steps:**

1.  **Robust RLS & Security Refinement**
    *   Refine and implement comprehensive RLS policies for all `public` tables (`users`, `companies`, `knowledge_bases`, `conversations`, `messages`).
    *   Implement JWT validation and user context extraction in FastAPI middleware for all API endpoints.

2.  **Conversation & Message Logging**
    *   Define `public.users` table.
    *   Define `public.conversations` table.
    *   Define `public.messages` table.
    *   Modify `backend/app/bot/handler.py` to log incoming user messages and outgoing bot responses to these new tables.

3.  **Admin UI Development (Frontend)**
    *   Set up a new React project within `multi-tenant-ai-bot/frontend/`.
    *   Integrate Shadcn UI components.
    *   Develop a basic Admin Dashboard:
        *   Login page (using Supabase Auth).
        *   Page to list existing companies.
        *   Page to add/edit company details.
        *   Page to manage a company's knowledge base.
    *   Implement FastAPI endpoints for the Admin UI.

4.  **Improved RAG & LLM Management**
    *   Explore and implement more sophisticated text chunking strategies.
    *   Evaluate and integrate a more capable open-source LLM.
    *   Implement basic prompt templating for the LLM.

5.  **Basic CI/CD & Deployment Automation**
    *   Set up basic CI/CD pipelines (e.g., GitHub Actions) for automated testing and deployment of the backend.

---

### **Plan 3: Advanced Features & Scalability**

**Objective:** To expand the system's capabilities, integrate with more platforms, and enhance its robustness and monitoring.

**Deliverables:**
*   WhatsApp integration.
*   Structured knowledge input.
*   Performance analytics.
*   Human handoff mechanism.

**Steps:**

1.  **WhatsApp Integration**
    *   Research and implement integration with the WhatsApp Business API.
    *   Extend `backend/app/bot/` to handle WhatsApp messages.

2.  **Structured Knowledge Input**
    *   Develop FastAPI endpoints and frontend UI for uploading structured data.
    *   Implement data parsing and ingestion logic.

3.  **Performance Analytics & Monitoring**
    *   Develop dashboards to visualize usage metrics, common queries, and unanswered questions.
    *   Implement robust logging and error tracking.

4.  **Human Handoff**
    *   Develop a mechanism to transfer conversations to human agents.
    *   Implement a way to notify a human agent.

5.  **Advanced AI Capabilities**
    *   Explore and implement more sophisticated conversational flows.
    *   Investigate proactive outreach or personalized recommendations.

6.  **Deployment Automation & Scaling Refinement**
    *   Optimize LLM inference for cost and speed.
    *   Refine deployment strategies for higher availability and scalability.
