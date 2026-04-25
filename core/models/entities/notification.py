from django.db import models


class Notification(models.Model):
    class Level(models.TextChoices):
        SUCCESS = 'SUCCESS', 'Success'
        ERROR = 'ERROR', 'Error'
        INFO = 'INFO', 'Info'

    creator = models.ForeignKey(
        'core.Creator', on_delete=models.CASCADE, related_name='notifications'
    )
    message = models.TextField()
    level = models.CharField(max_length=10, choices=Level.choices, default=Level.INFO)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.level}] {self.message[:60]}'
