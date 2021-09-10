from django.db import models


class Reaction(models.Model):
    """Create instances of the Reaction class"""
    label = models.CharField(max_length=50)
    image_url = models.TextField()
