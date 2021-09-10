from django.db import models
from django.contrib.auth.models import User

class AppUser(models.Model):
    """StressLess app user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    image_url = models.TextField()

    @property
    def full_name(self):
        """returns auth user full name"""
        return f'{self.user.first_name} {self.user.last_name}'
        