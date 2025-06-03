from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


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
    

class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)


    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid details', code='authentication')

        attrs['user'] = user

        return attrs
    

    def generate_tokens(self, attrs):
        user = attrs.get('user')

        refresh = RefreshToken.for_user(user)

        tokens = {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

        return tokens


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'username']

        read_only_fields = ['id', 'email']