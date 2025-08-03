from predict.models import DiseasePrediction
from rest_framework import serializers


class DiseasePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseasePrediction
        fields = ['id', 'user', 'image', 'prediction', 'confidence', 'timestamp']

        read_only_fields = ['id']