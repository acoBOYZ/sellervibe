from django.db import models
from django.conf import settings

class UserEmails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    emails = models.JSONField()