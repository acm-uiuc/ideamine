from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class Idea(models.Model):
    owner = models.ForeignKey(User, related_name='owned_ideas')
    short_name = models.CharField(max_length=50)
    desc = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='ideas')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    members = models.ManyToManyField(User, related_name='joined_ideas', through='JoinedUser', editable=False)

    def unconfirmed_members(self):
        return self.members.filter(joineduser__confirmed=False)

    def join_user(self, new_user):
        relation = JoinedUser(user=new_user, idea=self)
        return relation.save()
    
    def __unicode__(self):
        return self.short_name + ': ' + self.owner.username

class JoinedUser(models.Model):
    user = models.ForeignKey(User)
    idea = models.ForeignKey(Idea)
    confirmed = models.BooleanField(default=False, editable=False)
