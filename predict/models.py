import uuid
from accounts.models import User
from django.db import models


class DiseasePrediction(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='predictions/')
    prediction = models.CharField(max_length=50)
    confidence = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.prediction
    

    class Meta:
        ordering = ('-timestamp',)