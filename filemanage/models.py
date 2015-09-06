# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

LXREPORT = 1
LXTOOL = 2
LXFILE_SORT = (
    (LXREPORT, '报告'),
    (LXTOOL, '工具')
)


class LXFile(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    uploader = models.ForeignKey(User)
    createtime = models.DateTimeField(auto_now_add=True)
    sort = models.CharField(max_length=2, choices=LXFILE_SORT)
    remark = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name
