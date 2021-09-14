from django.db import models


class Priority(models.Model):
    """Priority Model"""
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateField()
    completed = models.BooleanField()

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        self.__owner = value
