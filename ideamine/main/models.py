from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    def delete_orphaned():
        for tag in Tag.objects.all():
            if not tag.ideas:
                tag.delete()

    @models.permalink
    def get_absolute_url(self):
        return ('tag_ideas', (), { 'object_name' : self.name })

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def username(self):
        return self.user.username

    def owned_idea_count(self):
        return self.owned_ideas.count()

    def joined_idea_count(self):
        return self.joined_ideas.count()

    def followers(self):
        users = dict()
        for idea in self.owned_ideas.all():
            users.update(dict.fromkeys(idea.members.all()))
        return len(users)

    def can_update_user(self, user):
        return self.user.has_perms('main.change_user') or user.pk == self.user.pk

    def can_update_idea(self, idea):
        return self.user.has_perms('main.change_idea') or idea.can_edit(self.user)

    def __unicode__(self):
        return self.username()

    @models.permalink
    def get_absolute_url(self):
        return ('user_detail', (), { 'object_id' : self.user.pk })

class Idea(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='owned_ideas')
    short_name = models.CharField(max_length=50, unique=True)
    desc = models.TextField(verbose_name='description')
    tags = models.ManyToManyField(Tag, related_name='ideas', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    members = models.ManyToManyField(UserProfile, related_name='joined_ideas',
                                     through='JoinedUser', editable=False)
    # TODO: Implement usage of progress in site functionality
    # Progress is a number between 0 and 100 representing percent complete
    progress = models.SmallIntegerField(default=0)
    website = models.URLField(blank=True, verify_exists=False)

    def confirm_member(self, user):
        try:
            joineduser = self.joineduser(user)
            joineduser.confirmed = True
            joineduser.save()
        except ObjectDoesNotExist:
            joineduser = JoinedUser(user=user.get_profile(), idea=self, confirmed=True)

    def can_edit(self, user):
        return self.is_confirmed(user) or self.is_owner(user)

    def can_destroy(self, user):
        return self.is_owner(user) or user.has_perms('main.delete_idea')

    def is_confirmed(self, user):
        try:
            self.confirmed_members().get(pk=user.get_profile().pk)
            return True
        except ObjectDoesNotExist:
            return False

    def is_member(self, user):
        try:
            self.members.get(user=user.get_profile().pk)
            return True
        except ObjectDoesNotExist:
            return False

    def is_owner(self, user):
        return self.owner.user.pk == user.pk

    def unconfirmed_members(self):
        return self.members.filter(joineduser__confirmed=False)

    def confirmed_members(self):
        return self.members.filter(joineduser__confirmed=True)

    def joineduser(self, user):
        return JoinedUser.objects.get(user=user.get_profile(), idea=self)

    def add_member(self, new_user):
        relation = JoinedUser(user=new_user.get_profile(), idea=self)
        return relation.save()

    def remove_member(self, user):
        joineduser = self.joineduser(user)
        return joineduser.delete()

    def tags_to_s(self):
        if self.tags.exists():
            return " ".join(map(Tag.__str__, self.tags.all()))
        return None

    def change_tags(self, tags_string):
        self.tags.clear()
        tag_list = tags_string.split()
        for tag_s in tag_list:
            try:
                tag = Tag.objects.get(name__iexact=tag_s)
                tag.ideas.add(self)
            except ObjectDoesNotExist:
                self.tags.create(name=tag_s)

    def __unicode__(self):
        return '%s: %s' % (self.short_name, self.owner)

    @models.permalink
    def get_absolute_url(self):
        return ('idea_detail', (), { 'object_id' : self.pk })

class JoinedUser(models.Model):
    user = models.ForeignKey(UserProfile)
    idea = models.ForeignKey(Idea)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

class Image(models.Model):
    def path(instance, filename):
       return 'images/%d/%s' % (instance.idea.pk, filename)

    def get_absolute_url(self):
        return self.image.url

    idea = models.ForeignKey(Idea, related_name='images')
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)
    uploader = models.ForeignKey(UserProfile, related_name='uploaded_images')
    image = models.ImageField(upload_to=path)
