from django.db import models
from django.conf import settings
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(        settings.AUTH_USER_MODEL,       # Reference to Django's user model
        on_delete=models.CASCADE,        # Required: specify delete behavior
        related_name='posts')