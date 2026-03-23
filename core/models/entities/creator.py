from django.db import models
from django.contrib.auth.models import User

class Creator(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  email = models.EmailField(unique=True)
  display_name = models.CharField(max_length=255)
  token_amount = models.IntegerField(default=0)

  def __str__(self):
    return self.display_name
