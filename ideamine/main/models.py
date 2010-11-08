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
    # Possibilities: related to MTMField class, related names must be unique
    #members = models.ManyToManyField(User, related_name='+')
    
    def __unicode__(self):
        return self.shortName + ': ' + self.owner

# Working on a better way to implement this
# Django models ids, so I don't think we need any other unique identifiers
class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='+')
    location = models.ForeignKey(Idea)
    parent = models.ForeignKey('self')
    text = models.CharField(max_length=2000)

    def __unicode__(self):
        return self.id + ': ' + self.owner + ' on ' + self.location
