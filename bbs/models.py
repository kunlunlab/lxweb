from django.db import models
from django.contrib.auth.models import User

class BBS(models.Model):
    title = models.CharField(max_length=128)
    summary = models.CharField(max_length=256, blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(User)
    view_count = models.IntegerField()
    ranking = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)



