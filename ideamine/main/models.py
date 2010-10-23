from django.db import models

class Idea(models.Model):
    owner = models.ForeignKey(User)
    shortName = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tag)
    members = models.ManyToManyField(User)

class Tag(models.Model):
    name = models.CharField(max_length=25)

# Working on a better way to implement this
class Comment(models.Model):
    owner = models.ForeignKey(User)
    location = models.ForeignKey(Idea)
    parent = models.ForeignKey(Comment)
    text = models.CharField(max_length=300)
