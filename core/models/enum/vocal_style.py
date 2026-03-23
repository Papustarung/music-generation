from django.db import models


class VocalStyle(models.TextChoices):
  MALE = 'MALE', 'Male'
  FEMALE = 'FEMALE', 'Female'
  DUET = 'DUET', 'Duet'
  INSTRUMENTAL = 'INSTRUMENTAL', 'Instrumental'
  RAP = 'RAP', 'Rap'
  OTHER = 'OTHER', 'Other'
