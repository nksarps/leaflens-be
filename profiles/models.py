import uuid
from accounts.models import User
from django.db import models


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True) # Add default profile
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"

    
    class Meta:
        ordering = ('-created_at',)
