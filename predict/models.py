from accounts.models import User
from django.db import models


class DiseasePrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='predictions/')
    prediction = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.prediction
    

    class Meta:
        ordering = ('-timestamp',)