from django.db import models
from .creator import Creator
from .song import Song
from ..enum import VocalStyle, JobStatus, Genre, Occasion

class GenerationJob(models.Model):
  creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
  song = models.OneToOneField(Song, on_delete=models.SET_NULL, null=True, blank=True)

  status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.QUEUED)
  requested_at = models.DateTimeField(auto_now_add=True)

  title = models.CharField(max_length=255)
  story = models.TextField()
  genre = models.CharField(max_length=50, choices=Genre.choices)
  vocal_style = models.CharField(max_length=50, choices=VocalStyle.choices)
  occasion = models.CharField(max_length=50, choices=Occasion.choices)
  lyrics = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"Job {self.id} - {self.status}"