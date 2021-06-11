import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.db.models.fields.reverse_related import ManyToOneRel


from .managers import UserManager

def content_file_name(instance, filename):
    print(instance)
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user_id, instance.user.last_name, ext)
    return os.path.join('profile_image', filename)



# Create your models here.
class User(AbstractUser):
    username = None
    
    # defining sex choices
    Male = 'M'
    Female = 'F'
    Undisclosed = 'U'

    SEX_CHOICES = [
        (Male, 'Male'),
        (Female, 'Female'),
        (Undisclosed, 'Undisclosed')
    ]

    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=Undisclosed)
    
    D_O_B = models.DateField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()


    def __str__(self):
        return self.last_name

class Profile_pic(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name="picture")
    profile_pic = models.ImageField(upload_to=content_file_name)

    objects = UserManager()

    def __self__(self):
        return self.profile_pic.url
