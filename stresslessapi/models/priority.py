from django.db import models


class Priority(models.Model):
    """Priority Model"""
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField()
    completed = models.BooleanField()
