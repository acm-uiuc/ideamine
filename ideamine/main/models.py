from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Tag(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class Idea(models.Model):
    owner = models.ForeignKey(User, related_name='ownedIdeas')
    shortName = models.CharField(max_length=50)
    desc = models.TextField()
    tags = models.ManyToManyField(Tag)
    createdAt = models.DateTimeField(blank=True)
    modifiedAt = models.DateTimeField(blank=True)
    members = models.ManyToManyField(User, related_name='joinedIdeas')
    
    def __unicode__(self):
        return self.shortName + ': ' + self.owner.username

    def save(self):
        if self.createdAt == None:
            self.createdAt = datetime.now()
        self.modifiedAt = datetime.now()
        super(Idea, self).save()

# Working on a better way to implement this
# Django models ids, so I don't think we need any other unique identifiers
class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments')
    location = models.ForeignKey(Idea)
    parent = models.ForeignKey('self')
    text = models.CharField(max_length=2000)
    createdAt = models.DateTimeField(blank=True)
    modifiedAt = models.DateTimeField(blank=True)

    def __unicode__(self):
        return self.id + ': ' + self.owner.username + ' on ' + self.location

    def save(self):
        if self.createdAt == None:
            self.createdAt = datetime.now()
        self.modifiedAt = datetime.now()
        super(Idea, self).save()
