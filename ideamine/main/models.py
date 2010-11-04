from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=25)

class Idea(models.Model):
    owner = models.ForeignKey(User, related_name='+')
    shortName = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tag)
    # So this line doesn't work. I don't know why (yet)
    #members = models.ManyToManyField(User, related_name='+')

# Working on a better way to implement this
class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='+')
    location = models.ForeignKey(Idea)
    parent = models.ForeignKey('self')
    text = models.CharField(max_length=300)
