from django.db import models


class Post(models.Model):
    """Post Model"""
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_url = models.TextField()
    publication_date = models.DateTimeField()

    @property
    def owner(self):
        """returns owner of post"""
        return self.__owner

    @owner.setter
    def owner(self, value):
        self.__owner = value
