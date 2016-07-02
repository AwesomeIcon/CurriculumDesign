# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Student(models.Model):
    SEX = (
        ('男', '男'),
        ('女', '女'),
    )
    uid = models.CharField(max_length=13, primary_key=True)
    uname = models.CharField(max_length=20)
    usex = models.CharField(max_length=2, choices=SEX)
    upasswd = models.CharField(max_length=32)


class Teacher(models.Model):
    SEX = (
        ('男', '男'),
        ('女', '女'),
    )
    tid = models.CharField(max_length=13, primary_key=True)
    tname = models.CharField(max_length=20)
    tsex = models.CharField(max_length=2, choices=SEX)
    ttitle = models.CharField(max_length=20, null=True)


class Course(models.Model):
    cid = models.CharField(max_length=10)
    cname = models.CharField(max_length=20)
    ccredit = models.FloatField()
    cclass = models.CharField(max_length=10)
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cid', 'tid')


class CSINFO(models.Model):
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    uid = models.ForeignKey(Student, on_delete=models.CASCADE)
    cid = models.ForeignKey(Course, on_delete=models.CASCADE)
    weight = models.IntegerField()

    class Meta:
        unique_together = ('tid', 'uid', 'cid')


class RecordLog(models.Model):
    uid = models.ForeignKey(Student, on_delete=models.CASCADE)
    operate = models.CharField(max_length=10)
    cid = models.ForeignKey(Course, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20)
    logtime = models.CharField(max_length=10)

    class Meta:
        ordering = ['-id']