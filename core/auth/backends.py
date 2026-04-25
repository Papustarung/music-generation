from django.contrib.auth.backends import ModelBackend
from core.models.entities.creator import Creator


class EmailBackend(ModelBackend):
    """Information Expert (GRASP) — knows how to authenticate a Creator by email."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Creator.objects.get(email=username)
        except Creator.DoesNotExist:
            try:
                user = Creator.objects.get(username=username)
            except Creator.DoesNotExist:
                return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Creator.objects.get(pk=user_id)
        except Creator.DoesNotExist:
            return None
