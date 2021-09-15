from django.db import models


class Reflection(models.Model):
    """Reflection Model"""
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    content = models.CharField(max_length=150)
    created_on = models.DateTimeField()

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        self.__owner = value
