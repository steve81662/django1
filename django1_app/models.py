from django.db import models
from django.contrib.auth.models import User


# UserProfileInfo will "extend" User, including some additional properties (portfolio and picture)
class UserProfileInfo(models.Model):
    # Create relationship between UserProfileInfo and User by defining a "user" one-to-one field
    # that ties the UserProfileInfo to a specific User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Define the additional fields that extend User
    portfolio = models.URLField(blank=True)

    # pip install pillow - required to use "upload_to"
    picture = models.ImageField(upload_to='profile_pics', blank=True)

    # Return the User Name when referencing obj.str()
    def __str__(self):
        return self.user.username
