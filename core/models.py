from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.UUIDField(primary_key=True, default=uuid.uuid4)
    api_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['api_key']),
        ]
        
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if self.api_key:
            self.api_key = str(self.api_key)  # convert UUID to string
        super(Profile, self).save(*args, **kwargs)
    