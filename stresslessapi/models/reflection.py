from django.db import models


class Reflection(models.Model):
    """Reflection Model"""
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    created_on = models.DateTimeField()
