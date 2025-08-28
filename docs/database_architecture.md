## 6. Database Architecture (Key Tables & Relationships)

Here are the essential tables and how they will relate to each other, integrating with Supabase's built-in authentication:

### Core Tables:

1.  **`auth.users` (Supabase Internal)**
    *   **Purpose:** Managed by Supabase for user authentication. We will not directly modify this table.

2.  **`public.users`**
    *   **Purpose:** Stores additional application-specific profile information for users.
    *   **Relationship:** **One-to-One** with `auth.users` (via `id`).

3.  **`public.companies`**
    *   **Purpose:** Central table for each business/tenant.
    *   **Key Identifiers:** `id` (Primary Key), `telegram_chat_id` (Unique, for linking to a Telegram channel/group).
    *   **Relationships:**
        *   **One-to-Many** with `public.knowledge_bases`.
        *   **One-to-Many** with `public.conversations`.

4.  **`public.knowledge_bases`**
    *   **Purpose:** Stores the raw, unstructured knowledge content for each company.
    *   **Relationship:** **Many-to-One** with `public.companies` (via `company_id`).

5.  **`public.conversations`**
    *   **Purpose:** Stores the history of interactions (sessions) between users and the bot.
    *   **Relationships:**
        *   **Many-to-One** with `public.companies` (via `company_id`).
        *   **Many-to-One** with `public.users` (via `user_id`).
        *   **One-to-Many** with `public.messages`.

6.  **`public.messages`**
    *   **Purpose:** Stores individual messages within a `conversation`.
    *   **Relationship:** **Many-to-One** with `public.conversations` (via `conversation_id`).

### Summary of Relationships:

```
+-----------------+       +-----------------+       +-------------------+
|   auth.users    |-------|   public.users  |       |                   |
| (Supabase Auth) | 1   1 | (App Profiles)  |       |                   |
+-----------------+       +-----------------+       |                   |
                                   | 1               |                   |
                                   |                 |                   |
                                   | M               |                   |
                                   |                 |                   |
+-----------------+       +-----------------+       |                   |
| public.companies|-------|public.conversations|-----| public.messages   |
| (Tenants)       | 1   M | (User Sessions) | 1   M | (Individual Msgs) |
+-----------------+       +-----------------+       +-------------------+
         | 1
         |
         | M
         |
+---------------------+
| public.knowledge_bases|
| (Company Data)      |
+---------------------+
```