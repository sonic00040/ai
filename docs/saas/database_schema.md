# SaaS Database Schema

This document provides the SQL statements for setting up the database schema for the SaaS platform. This script is idempotent, meaning it can be run multiple times without causing errors.

---

```sql
-- Modify the "companies" table
ALTER TABLE companies
DROP COLUMN IF EXISTS telegram_chat_id;

ALTER TABLE companies
ADD COLUMN IF NOT EXISTS telegram_bot_token TEXT UNIQUE,
ADD COLUMN IF NOT EXISTS whatsapp_identifier TEXT UNIQUE;

-- Create the "plans" table
CREATE TABLE IF NOT EXISTS plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    token_limit BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Create the "subscriptions" table
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id),
    plan_id UUID NOT NULL REFERENCES plans(id),
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Create the "usage_logs" table
CREATE TABLE IF NOT EXISTS usage_logs (
    id BIGSERIAL PRIMARY KEY,
    subscription_id UUID NOT NULL REFERENCES subscriptions(id),
    total_tokens INT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## 5. Create `get_total_usage` SQL Function

This function efficiently calculates the total token usage for a given subscription within a date range. It is called via RPC from our backend.

```sql
CREATE OR REPLACE FUNCTION get_total_usage(
    p_subscription_id UUID,
    p_start_date TIMESTAMPTZ,
    p_end_date TIMESTAMPTZ
)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    total_usage INT;
BEGIN
    SELECT COALESCE(SUM(total_tokens), 0)
    INTO total_usage
    FROM usage_logs
    WHERE subscription_id = p_subscription_id
      AND timestamp >= p_start_date
      AND timestamp < p_end_date;
      
    RETURN total_usage;
END;
$$;
```
