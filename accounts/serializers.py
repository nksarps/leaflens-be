from accounts.models import User
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'username', 'password', 'created_at']

        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(
            first_name=validated_data.get('first_name'),
            middle_name=validated_data.get('middle_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            username=validated_data.get('username'),
        )

        user.set_password(password)
        user.save()

        return user