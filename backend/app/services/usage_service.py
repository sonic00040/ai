import logging
from uuid import UUID
from app.services.supabase_service import supabase_service

logger = logging.getLogger(__name__)

class UsageService:
    def record_usage(self, *, subscription_id: UUID, total_tokens: int):
        """
        Records the token usage for a given subscription.
        """
        if not subscription_id or total_tokens <= 0:
            return

        try:
            supabase_service.add_usage_log(
                subscription_id=str(subscription_id),
                total_tokens=total_tokens
            )
            logger.info(f"Successfully logged {total_tokens} tokens for subscription {subscription_id}")
        except Exception as e:
            logger.error(f"An error occurred while recording usage for subscription {subscription_id}: {e}", exc_info=True)

    def has_exceeded_limit(self, subscription: dict) -> bool:
        """
        Checks if a subscription has exceeded its token limit for the current billing period.
        """
        try:
            subscription_id = subscription['id']
            plan_id = subscription['plan_id']
            start_date = subscription['start_date']
            end_date = subscription['end_date']

            # Get the plan details to find the token limit
            plan = supabase_service.get_plan_by_id(plan_id)
            if not plan:
                logger.error(f"Could not find plan with ID {plan_id} for subscription {subscription_id}")
                # Fail open or closed? For now, let's fail open (allow usage).
                return False
            
            token_limit = plan['token_limit']

            # Get the current usage for the billing period
            current_usage = supabase_service.get_usage_for_subscription(
                subscription_id=subscription_id,
                start_date=start_date,
                end_date=end_date
            )

            logger.info(f"Subscription {subscription_id}: Usage={current_usage}, Limit={token_limit}")

            return current_usage >= token_limit

        except Exception as e:
            logger.error(f"An error occurred while checking usage limit for subscription {subscription['id']}: {e}", exc_info=True)
            # Fail open in case of error to avoid blocking users.
            return False

usage_service = UsageService()