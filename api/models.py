from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

import os
import string

def generate_random_string(length, stringset=string.ascii_letters+string.digits):
    '''
    Returns a string with `length` characters chosen from `stringset`
    >>> len(generate_random_string(20) == 20
    '''
    return ''.join([stringset[i%len(stringset)] \
        for i in [ord(x) for x in os.urandom(length)]])

def generate_key():
    return generate_random_string(32)

# Create your models here.
class Key(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=32, default=generate_key, unique=True)
    created_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = (("user", "name"),)
