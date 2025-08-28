# SaaS MVP Development Plan

This document outlines the development phases for building the Minimum Viable Product (MVP) of the SaaS platform.

## Phase 1: Database Foundation

**Goal:** Update the database schema to support multi-tenancy and subscription logic.

1.  **Modify `companies` Table:**
    -   Remove the `telegram_chat_id` column.
    -   Add a `telegram_bot_token` column to store the unique token for each company's Telegram bot.
    -   Add a `whatsapp_identifier` column (nullable) for future WhatsApp integration.
2.  **Create `plans` Table:**
    -   Create a new table to store the details of the subscription plans (name, price, token_limit).
3.  **Create `subscriptions` Table:**
    -   Create a new table to link a company to a plan and track their billing cycle (start_date, end_date, is_active).
4.  **Create `usage_logs` Table:**
    -   Create a new table to record every API call's token usage for each subscription.

## Phase 2: Backend Logic Implementation

**Goal:** Implement the core SaaS logic for usage metering and limit enforcement.

1.  **Update Tenant Identification:**
    -   Modify the `handle_message` function in the bot handler to identify the company based on the incoming `telegram_bot_token`.
2.  **Implement Usage Metering:**
    -   Modify the `rag_service` to accurately count and return the total tokens used for each `generate_response_with_llm` call.
    -   Create a new `UsageService` that contains a `record_usage` function to log the token count in the `usage_logs` table after every successful API call.
3.  **Implement Limit Enforcement:**
    -   In the `UsageService`, create a `check_usage` function that calculates the total tokens used by a subscription in the current billing period.
    *   In the `handle_message` function, before processing a message, call the `check_usage` function to see if the company has exceeded its limit.
    *   If the limit is exceeded, the bot will send a "limit reached" message and stop.

## Phase 3: Frontend MVP - Dashboard

**Goal:** Build the minimum viable dashboard for clients to manage their service.

1.  **Project Setup:**
    -   Initialize a new React application for the frontend dashboard.
2.  **User Authentication:**
    -   Implement user registration and login functionality (e.g., using Supabase Auth).
3.  **Company & Channel Configuration:**
    -   Build the UI for the user onboarding flow as defined in `architecture.md`. This includes forms for creating a company, selecting a plan, and submitting channel credentials (e.g., Telegram Bot Token).
4.  **Usage Dashboard:**
    -   Create a simple dashboard page that displays the user's current plan and their token usage for the current billing cycle.
    -   This will fetch data from a new API endpoint that exposes the usage data from the `usage_logs` table.
5.  **Knowledge Base Management:**
    -   Build the UI for clients to upload and manage their knowledge base documents.

## Phase 4: Future Development

**Goal:** Plan for the implementation of premium features after the MVP is launched.

1.  **Implement Premium Features:**
    -   Begin development on the features outlined in `plans.md`, such as Analytics, Integrations, and Customization options.
2.  **Payment Integration:**
    -   Integrate a payment provider like Stripe to automate the subscription and billing process.
3.  **Testing & Deployment:**
    -   Thoroughly test the entire platform.
    -   Deploy the backend and frontend applications.
