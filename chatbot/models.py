from accounts.models import User
from django.db import models


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, db_index=True)
    sender = models.CharField(max_length=25)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.sender} ({self.session_id}): {self.message[:50]}'

    class Meta:
        ordering = ('-timestamp',)