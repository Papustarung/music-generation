from django.db import models


class Genre(models.TextChoices):
  JAZZ = 'JAZZ', 'Jazz'
  ROCK = 'ROCK', 'Rock'
  POP = 'POP', 'Pop'
  HIPHOP = 'HIPHOP', 'Hip Hop'
  CLASSICAL = 'CLASSICAL', 'Classical'
  EDM = 'EDM', 'EDM'
  RNB = 'RNB', 'R&B'
  FOLK = 'FOLK', 'Folk'
  METAL = 'METAL', 'Metal'
  OTHER = 'OTHER', 'Other'
