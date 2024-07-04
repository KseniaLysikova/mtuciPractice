from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=255)
    salary = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    experience = models.CharField(max_length=255, null=True, blank=True)
    work_format = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255)
    employer = models.CharField(max_length=255)
    url = models.URLField(unique=True, null=True)
