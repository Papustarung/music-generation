from django.db import models
from .creator import Creator

class Library(models.Model):
  creator = models.OneToOneField(Creator, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.creator.display_name}'s Library"