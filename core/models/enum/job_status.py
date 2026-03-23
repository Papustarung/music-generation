from django.db import models


class JobStatus(models.TextChoices):
  QUEUED = 'QUEUED', 'Queued'
  GENERATING = 'GENERATING', 'Generating'
  COMPLETED = 'COMPLETED', 'Completed'
  FAILED = 'FAILED', 'Failed'
