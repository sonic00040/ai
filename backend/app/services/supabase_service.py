from supabase import create_client, Client
from app.core.config import settings
from typing import List, Dict, Any
from postgrest.exceptions import APIError # Import APIError

class SupabaseService:
    def __init__(self):
        self.supabase_url: str = settings.SUPABASE_URL
        self.supabase_key: str = settings.SUPABASE_KEY
        self.client: Client = create_client(self.supabase_url, self.supabase_key)

    # --- Company Functions ---
    def get_company_by_telegram_bot_token(self, telegram_bot_token: str) -> Dict[str, Any] | None:
        """Fetches company details by Telegram bot token."""
        try:
            response = self.client.from_('companies').select('*').eq('telegram_bot_token', telegram_bot_token).maybe_single().execute()
            if response.data:
                return response.data
            return None
        except APIError as e:
            print(f"Error getting company by token: {e}")
            return None

    def get_company_by_name(self, name: str) -> Dict[str, Any] | None:
        """Fetches company details by name."""
        try:
            response = self.client.from_('companies').select('*').eq('name', name).maybe_single().execute()
            if response.data:
                return response.data
            return None
        except APIError as e:
            print(f"Error getting company by name: {e}")
            return None

    def get_all_bot_tokens(self) -> List[str]:
        """Fetches all telegram_bot_tokens from the companies table."""
        response = self.client.from_('companies').select('telegram_bot_token').execute()
        if response.data:
            return [company['telegram_bot_token'] for company in response.data if company.get('telegram_bot_token')]
        return []

    def add_company(self, name: str, telegram_bot_token: str) -> Dict[str, Any] | None:
        """Adds a new company to the database."""
        response = self.client.from_('companies').insert({'name': name, 'telegram_bot_token': telegram_bot_token}).execute()
        if response.data:
            return response.data[0]
        return None

    # --- KnowledgeBase Functions ---
    def get_knowledge_bases_by_company_id(self, company_id: str) -> List[Dict[str, Any]]:
        """Fetches all knowledge base entries for a given company ID."""
        response = self.client.from_('knowledge_bases').select('*').eq('company_id', company_id).execute()
        if response.data:
            return response.data
        return []

    def add_knowledge_base_entry(self, company_id: str, content: str, embedding: List[float]) -> Dict[str, Any] | None:
        """Adds a new knowledge base entry for a company."""
        response = self.client.from_('knowledge_bases').insert({'company_id': company_id, 'content': content, 'embedding': embedding}).execute()
        if response.data:
            return response.data[0]
        return None

    # --- Plan & Subscription Functions ---
    def get_plan_by_id(self, plan_id: str) -> Dict[str, Any] | None:
        """Fetches plan details by plan ID."""
        try:
            response = self.client.from_('plans').select('*').eq('id', plan_id).maybe_single().execute()
            if response.data:
                return response.data
            return None
        except APIError as e:
            print(f"Error getting plan by ID: {e}")
            return None

    def get_plan_by_name(self, name: str) -> Dict[str, Any] | None:
        """Fetches plan details by name."""
        try:
            response = self.client.from_('plans').select('*').eq('name', name).maybe_single().execute()
            if response.data:
                return response.data
            return None
        except APIError as e:
            print(f"Error getting plan by name: {e}")
            return None

    def add_plan(self, name: str, price: float, token_limit: int) -> Dict[str, Any] | None:
        """Adds a new subscription plan."""
        response = self.client.from_('plans').insert({
            'name': name,
            'price': price,
            'token_limit': token_limit
        }).execute()
        if response.data:
            return response.data[0]
        return None

    def get_active_subscription_by_company_id(self, company_id: str) -> Dict[str, Any] | None:
        """Fetches the active subscription for a given company ID."""
        try:
            response = self.client.from_('subscriptions').select('*').eq('company_id', company_id).eq('is_active', True).maybe_single().execute()
            if response.data:
                return response.data
            return None
        except APIError as e:
            print(f"Error getting active subscription: {e}")
            return None

    def add_subscription(self, company_id: str, plan_id: str, start_date: str, end_date: str) -> Dict[str, Any] | None:
        """Adds a new subscription for a company."""
        response = self.client.from_('subscriptions').insert({
            'company_id': company_id,
            'plan_id': plan_id,
            'start_date': start_date,
            'end_date': end_date,
            'is_active': True
        }).execute()
        if response.data:
            return response.data[0]
        return None

    # --- Usage Functions ---
    def get_usage_for_subscription(self, subscription_id: str, start_date: str, end_date: str) -> int:
        """Calculates the total token usage for a subscription within a date range."""
        try:
            response = self.client.rpc('get_total_usage', {
                'p_subscription_id': subscription_id,
                'p_start_date': start_date,
                'p_end_date': end_date
            }).execute()
            
            if response.data:
                return response.data
            return 0
        except Exception as e:
            print(f"Error getting usage: {e}")
            return 0

    def add_usage_log(self, subscription_id: str, total_tokens: int) -> None:
        """Adds a new usage log entry."""
        try:
            self.client.from_('usage_logs').insert({
                'subscription_id': subscription_id,
                'total_tokens': total_tokens
            }).execute()
        except Exception as e:
            print(f"Error logging usage: {e}")

supabase_service = SupabaseService()