from accounts.serializers import UserSerializer
from profiles.models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'phone_number', 'location']

        read_only_fields = ['id', 'user']

