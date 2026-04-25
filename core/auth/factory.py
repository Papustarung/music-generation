from .strategies.password_strategy import PasswordAuthStrategy
from .strategies.google_strategy import GoogleAuthStrategy
from .strategies.base import AuthStrategy


class AuthStrategyFactory:
    """Creator (GRASP) — knows how to instantiate the right AuthStrategy."""

    _registry = {
        'password': PasswordAuthStrategy,
        'google': GoogleAuthStrategy,
    }

    @classmethod
    def get_strategy(cls, auth_type: str) -> AuthStrategy:
        strategy_class = cls._registry.get(auth_type)
        if strategy_class is None:
            raise ValueError(f"Unknown auth type: '{auth_type}'. Valid types: {list(cls._registry)}")
        return strategy_class()
