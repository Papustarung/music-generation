from .base import AuthStrategy, AuthResult
from core.models.entities.creator import Creator
from core.models.entities.oauth_profile import OAuthProfile

class GoogleAuthStrategy(AuthStrategy):
	def authenticate(self, **credentials) -> AuthResult:
		google_id = credentials["google_id"]
		email = credentials["email"]
		name = credentials.get("name", "")
		access_token = credentials.get("access_token", "")
		refresh_token = credentials.get("refresh_token", "")

		profile = OAuthProfile.objects.filter(
			provider="google", provider_user_id=google_id
		).select_related('creator').first()

		if profile:
			profile.access_token = access_token
			profile.refresh_token = refresh_token
			profile.save(update_fields=["access_token", "refresh_token"])
			return AuthResult(success=True, creator=profile.creator)

		return self.register(
			google_id=google_id,
			email=email,
			name=name,
			access_token=access_token,
			refresh_token=refresh_token,
		)

	def register(self, **data) -> AuthResult:
		creator, _ = Creator.objects.get_or_create(
			email=data["email"],
			defaults={
				"username": data["email"],
				"display_name": data.get("name", data.get("display_name", "")),
			},
		)
		OAuthProfile.objects.get_or_create(
			provider="google",
			provider_user_id=data["google_id"],
			defaults={
				"creator": creator,
				"access_token": data.get("access_token", ""),
				"refresh_token": data.get("refresh_token", ""),
			},
		)
		return AuthResult(success=True, creator=creator)