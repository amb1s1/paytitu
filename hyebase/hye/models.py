from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    interest = models.CharField(max_length=244, null=True)
    contact = models.CharField(max_length=100, null=True)
    
class Follow(models.Model):
    user = models.ForeignKey(User)
    followed_user = models.IntegerField(max_length=10)