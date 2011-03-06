from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class Tag(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def username(self):
        return self.user.username

    def __unicode__(self):
        return self.username()

class Idea(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='owned_ideas')
    short_name = models.CharField(max_length=50, unique=True)
    desc = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='ideas', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    members = models.ManyToManyField(UserProfile, related_name='joined_ideas',
                                     through='JoinedUser', editable=False)

    def confirm_member(self, user):
        try:
            joineduser = self.joineduser(user)
            joineduser.confirmed = True
            joineduser.save()
        except ObjectDoesNotExist:
            joineduser = JoinedUser(user=user.get_profile(), idea=self, confirmed=True)

    def unconfirmed_members(self):
        return self.members.filter(joineduser__confirmed=False)

    def joineduser(self, user):
        return JoinedUser.objects.get(user=user.get_profile(), idea=self)

    def add_member(self, new_user):
        relation = JoinedUser(user=new_user.get_profile(), idea=self)
        return relation.save()

    def remove_member(self, user):
        joineduser = self.joineduser(user.get_picture())
        return joineduser.delete()

    def add_tags(self, tags_string):
        tag_list = tags_string.split()
        for tag in tag_list:
            self.tags.create(name=tag)

    def __unicode__(self):
        return self.short_name + ': ' + self.owner.username

    @models.permalink
    def get_absolute_url(self):
        return ('idea_detail', (), { 'object_id' : self.pk })

class JoinedUser(models.Model):
    user = models.ForeignKey(UserProfile)
    idea = models.ForeignKey(Idea)
    confirmed = models.BooleanField(default=False, editable=False)
