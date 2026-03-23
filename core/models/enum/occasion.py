from django.db import models


class Occasion(models.TextChoices):
  BIRTHDAY = 'BIRTHDAY', 'Birthday'
  WEDDING = 'WEDDING', 'Wedding'
  STUDY = 'STUDY', 'Study'
  WORKOUT = 'WORKOUT', 'Workout'
  PARTY = 'PARTY', 'Party'
  RELAX = 'RELAX', 'Relax'
  OTHER = 'OTHER', 'Other'
