from django.db import models


class PostReaction(models.Model):
    """Create instances of the Reaction class"""
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)