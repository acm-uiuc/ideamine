from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Tag(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class Idea(models.Model):
    owner = models.ForeignKey(User, related_name='owned_ideas')
    short_name = models.CharField(max_length=50)
    desc = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(blank=True)
    modified_at = models.DateTimeField(blank=True)
    members = models.ManyToManyField(User, related_name='joined_ideas')
    
    def __unicode__(self):
        return self.short_name + ': ' + self.owner.username

    def save(self):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.modified_at = datetime.now()
        super(Idea, self).save()

# Working on a better way to implement this
# Django models ids, so I don't think we need any other unique identifiers
class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments')
    location = models.ForeignKey(Idea)
    parent = models.ForeignKey('self')
    text = models.CharField(max_length=2000)
    created_at = models.DateTimeField(blank=True)
    modified_at = models.DateTimeField(blank=True)

    def __unicode__(self):
        return self.id + ': ' + self.owner.username + ' on ' + self.location

    def save(self):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.modified_at = datetime.now()
        super(Idea, self).save()
