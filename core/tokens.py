from datetime import date

from django.conf import settings

DAILY_GRANT = settings.DAILY_TOKEN_GRANT
MAX_BALANCE = settings.TOKEN_MAX_BALANCE
COST = settings.TOKEN_COST_PER_GENERATION


def replenish_if_needed(creator) -> bool:
    """
    Grant daily tokens if the creator hasn't been replenished today.
    Returns True if tokens were added.
    """
    today = date.today()
    if creator.last_token_replenish == today:
        return False

    creator.token_amount = min(creator.token_amount + DAILY_GRANT, MAX_BALANCE)
    creator.last_token_replenish = today
    creator.save(update_fields=['token_amount', 'last_token_replenish'])
    return True


def has_enough(creator) -> bool:
    return creator.token_amount >= COST


def deduct(creator) -> None:
    creator.token_amount = max(0, creator.token_amount - COST)
    creator.save(update_fields=['token_amount'])
