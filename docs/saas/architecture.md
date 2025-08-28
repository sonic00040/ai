# SaaS Architecture v2

This document outlines the architecture for the multi-tenant, multi-channel AI customer response system.

## 1. High-Level Overview

The system is designed as a Software as a Service (SaaS) platform where businesses (tenants) can subscribe to a plan and deploy a customized AI assistant on various communication channels (e.g., Telegram, WhatsApp).

The core architectural principle is **"one unique channel identifier per company,"** which allows for robust multi-tenancy and scalability.

## 2. System Components

-   **Backend:** A central FastAPI (Python) application that serves as the hub for all logic. It handles incoming messages from all channels, manages user subscriptions, tracks API usage, and interacts with the database and the LLM.
-   **Database:** A Supabase (PostgreSQL) database that stores all data, including company information, subscription plans, usage logs, and knowledge bases.
-   **LLM:** Google Gemini (specifically, the `gemini-1.5-flash` model for the MVP) is used for generating AI responses.
-   **Frontend:** A React-based web application that serves as the customer-facing dashboard for businesses to manage their accounts, subscriptions, and knowledge bases.

## 3. Core Logic: Tenant Identification

To ensure that every incoming message is correctly associated with the right company, we use the following identification strategy:

-   **Each company gets a unique bot/channel instance.** For example, for each company using Telegram, a new Telegram Bot is created, providing a unique `TELEGRAM_BOT_TOKEN`.
-   This unique token (or a similar identifier for other channels like WhatsApp) is stored in the `companies` table in our database.
-   The backend application listens to all registered bot tokens. When a message arrives, the backend first inspects the token to identify the company.
-   All subsequent logic (knowledge base retrieval, usage tracking, limit enforcement) is then performed in the context of that specific company.

This approach is secure, scalable, and allows for seamless integration of new channels in the future.

## 4. User Onboarding Flow

This section describes the step-by-step journey for a new business owner signing up for the service.

1.  **Account Creation:** The user first creates an account on the frontend dashboard using their email and a password.
2.  **Plan Selection:** The user is presented with the available subscription tiers and selects a plan that fits their needs.
3.  **Company Profile:** The user enters their company's name and other relevant details.
4.  **Channel Configuration:**
    -   The user chooses their desired communication channel (e.g., Telegram).
    -   The UI then prompts them for the necessary credentials for that channel. For Telegram, this is the **Bot Token**.
    -   The UI will provide helpful links and guides to assist the user in obtaining these credentials.
5.  **Backend Provisioning:**
    -   Upon submission, the frontend sends the collected information to the backend API.
    -   The backend creates the new `company` record, saves the unique channel identifier (`telegram_bot_token`), and creates the `subscription` record, linking the company to their chosen plan.
6.  **Initial Knowledge Base Upload:** After successful configuration, the user is redirected to the knowledge base management section of the dashboard to upload their documents and activate their AI assistant.
