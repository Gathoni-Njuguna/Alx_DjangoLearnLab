from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # unique reverse name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # unique reverse name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    def __str__(self):
        return self.name
    
# Create your models here.
