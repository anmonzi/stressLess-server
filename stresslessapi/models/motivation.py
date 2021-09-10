from django.db import models


class Motivation(models.Model):
    """Motivation Model"""
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_on = models.DateTimeField()
