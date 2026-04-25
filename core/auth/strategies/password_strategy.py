from django.contrib.auth import authenticate as django_authenticate
from .base import AuthStrategy, AuthResult
from core.models.entities.creator import Creator

class PasswordAuthStrategy(AuthStrategy):
	def authenticate(self, **credentials) -> AuthResult:
		user = django_authenticate(
			username=credentials.get('username'),
			password=credentials.get('password')
		)
		if user:
			return AuthResult(success=True, creator=user)
		return AuthResult(success=False, error='Invalid username or password.')

	def register(self, **data) -> AuthResult:
		if Creator.objects.filter(email=data["email"]).exists():
			return AuthResult(success=False, error='Email already registered.')
		user = Creator.objects.create_user(
			username=data["email"],
			email=data["email"],
			password=data["password"],
			display_name=data.get("display_name", data["email"])
		)
		return AuthResult(success=True, creator=user)