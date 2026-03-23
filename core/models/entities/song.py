from django.db import models
from .library import Library
from ..enum import Genre, VocalStyle, Occasion, Visibility

class Song(models.Model):
  library = models.ForeignKey(Library, on_delete=models.CASCADE)
  title = models.CharField(max_length=255)
  story = models.TextField()
  genre = models.CharField(max_length=20, choices=Genre.choices)
  vocal_style = models.CharField(max_length=20, choices=VocalStyle.choices)
  occasion = models.CharField(max_length=20, choices=Occasion.choices)
  visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.PRIVATE)
  lyrics = models.TextField(blank=True, null=True)
  audio_location = models.CharField(max_length=500, blank=True, null=True)

  def __str__(self):
    return self.title
