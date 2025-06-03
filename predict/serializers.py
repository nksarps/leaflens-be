from predict.models import DiseasePrediction
from rest_framework import serializers


class DiseasePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseasePrediction
        fields = ['user', 'image', 'prediction', 'timestamp']