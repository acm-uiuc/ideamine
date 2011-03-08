from django.db.models.signals import post_save
from django.contrib.comments.signals import comment_will_be_posted

from main.models import *

def user_profile_create(sender, **kwargs):
    if kwargs['created']:
        profile = UserProfile(user=kwargs['instance']);
        profile.save();

def validate_membership(sender, comment, **kwargs):
    if not comment.user:
        return False

post_save.connect(user_profile_create, sender=User)
comment_will_be_posted.connect(validate_membership)
