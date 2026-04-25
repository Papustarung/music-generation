from django.db import models
from django.contrib.auth.models import AbstractUser

class Creator(AbstractUser):
  email = models.EmailField(unique=True)
  display_name = models.CharField(max_length=255)
  token_amount = models.IntegerField(default=0)
  last_token_replenish = models.DateField(null=True, blank=True)

  def __str__(self):
    return self.display_name
