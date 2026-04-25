from django.db import models
from django.conf import settings

class OAuthProfile(models.Model):
	PROVIDER_CHOICES = [
		('google', 'Google'),
	]

	creator = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='oauth_profiles'
	)
	provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
	provider_user_id = models.CharField(max_length=255)
	access_token = models.CharField(max_length=255, blank=True)
	refresh_token = models.CharField(max_length=255, blank=True)

	class Meta:
		unique_together = ('provider', 'provider_user_id')