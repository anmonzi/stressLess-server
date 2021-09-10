from django.db import models


class Comment(models.Model):
    """Comment Model"""
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField()

    @property
    def owner(self):
        """returns owner of comment"""
        return self.__owner

    @owner.setter
    def owner(self, value):
        self.__owner = value
