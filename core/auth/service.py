from django.contrib.auth import login as django_login
from .factory import AuthStrategyFactory
from .strategies.base import AuthResult


class AuthService:
    """Controller (GRASP) — handles auth use cases; keeps views thin."""

    BACKEND = 'core.auth.backends.EmailBackend'

    def __init__(self, auth_type: str):
        self.strategy = AuthStrategyFactory.get_strategy(auth_type)

    def authenticate(self, request, **credentials) -> AuthResult:
        result = self.strategy.authenticate(**credentials)
        if result.success:
            django_login(request, result.creator, backend=self.BACKEND)
        return result

    def register(self, request, **data) -> AuthResult:
        result = self.strategy.register(**data)
        if result.success:
            django_login(request, result.creator, backend=self.BACKEND)
        return result
