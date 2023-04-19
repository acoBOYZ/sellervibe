from django.db import models
from django.contrib.auth.models import User

class UserJSON(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    json_file = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name