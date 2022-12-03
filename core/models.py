from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.UUIDField(default=0)
    api_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    