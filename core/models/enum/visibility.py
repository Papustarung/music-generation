from django.db import models


class Visibility(models.TextChoices):
  PRIVATE = 'PRIVATE', 'Private'
  SHARED = 'SHARED', 'Shared'
