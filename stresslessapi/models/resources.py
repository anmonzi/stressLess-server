from django.db import models


class Resources(models.Model):
    """Resource Model"""
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    source_link = models.TextField()
    created_on = models.DateTimeField()
