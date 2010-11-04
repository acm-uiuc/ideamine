from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class Idea(models.Model):
    owner = models.ForeignKey(User, related_name='+')
    shortName = models.CharField(max_length=50)
    desc = models.CharField(max_length=5000)
    tags = models.ManyToManyField(Tag)
    # So this line doesn't work. I don't know why (yet)
    #members = models.ManyToManyField(User, related_name='+')
    
    def __unicode__(self):
        return self.shortName + ': ' + self.owner

# Working on a better way to implement this
# Note ambiguity is present in the fields; working on this (hence no unicode call yet)
class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='+')
    location = models.ForeignKey(Idea)
    parent = models.ForeignKey('self')
    text = models.CharField(max_length=2000)
