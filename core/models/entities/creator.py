from django.db import models

class Creator(models.Model):
  email = models.EmailField(unique=True)
  display_name = models.CharField(max_length=255)
  token_amount = models.IntegerField(default=0)

  def __str__(self):
    return self.display_name
