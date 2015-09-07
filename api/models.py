from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Key(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=512)
    create_at = models.DateTimeField()
