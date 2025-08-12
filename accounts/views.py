import os, jwt
from accounts.models import User
from accounts.serializers import SignUpSerializer, LogInSerializer, UserSerializer
from accounts.utils import send_confirmation_mail, send_password_reset_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken



load_dotenv()


@api_view(['POST'])
def sign_up(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = User.objects.get(email=serializer.validated_data['email'])
            token = RefreshToken.for_user(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('verify_user')
            absolute_url = f'http://{current_site}{relative_link}?token={token}'
            link = str(absolute_url)
            send_confirmation_mail(email=user.email, first_name=user.first_name, link=link)

            return Response({
                'success':True,
                'message':'Email has been sent to the address you provided. Verify email account to log in.'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success':False,
            'message':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

def verify_user(request):
    if request.method == 'GET':
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return render(request, 'email_verified.html')
            
        except jwt.ExpiredSignatureError as e:
            return render(request, 'verification_error.html', {
                'error_title': 'Activation Link Expired',
                'error_message': 'The activation link has expired. Please request a new verification email from your LeafLens app.'
            }, status=400)
        except jwt.exceptions.DecodeError as e:
            return render(request, 'verification_error.html', {
                'error_title': 'Invalid Token',
                'error_message': 'The verification link is invalid. Please check your email and try again.'
            }, status=400)
        except jwt.exceptions.InvalidTokenError as e:
            return render(request, 'verification_error.html', {
                'error_title': 'Invalid Token',
                'error_message': 'The verification link is invalid. Please check your email and try again.'
            }, status=400)
        except User.DoesNotExist as e:
            return render(request, 'verification_error.html', {
                'error_title': 'User Not Found',
                'error_message': 'The user account could not be found. Please contact support if you believe this is an error.'
            }, status=404)
        except Exception as e:
            return render(request, 'verification_error.html', {
                'error_title': 'Verification Error',
                'error_message': 'An error occurred during verification. Please try again later or contact support.'
            }, status=400)


@api_view(['POST'])
def log_in(request):
    if request.method == 'POST':
        serializer = LogInSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            tokens = serializer.generate_tokens(serializer.validated_data)

            return Response({
                'success':True,
                'message':tokens
            }, status=status.HTTP_200_OK)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_reset(request):
    if request.method == 'POST':
        email = request.data.get('email')

        if not email:
            return Response({
                'success':False,
                'message':'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request).domain
            relative_link = reverse('password_reset_confirm')
            absolute_url = f'http://{current_site}{relative_link}?uid={uid}&token={token}'
            link = str(absolute_url)
            send_password_reset_mail(email=user.email, first_name=user.first_name, link=link)

            return Response({
                'success':True,
                'message':'Password reset mail sent'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            return Response (
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response (
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['PUT', 'PATCH'])
def password_reset_confirm(request):
    if request.method == 'PUT' or request.method == 'PATCH':
        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        if not uid or not token or not password:
            return Response (
                {
                    'success':False,
                    'message':'All fields are required'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(id=user_id)

            if not default_token_generator.check_token(user, token):
                return Response({
                    'success':True,
                    'message':'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()

            return Response({
                'success':True,
                'message':'Password reset successful'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            return Response (
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response (
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )
        

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    if request.method == 'PUT' or request.method == 'PATCH':
        user = request.user

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response({
                'success':True,
                'message':'User information successfully updated',
                'user':serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success':False,
            'message':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)

        return Response({
            'success':True,
            'user':serializer.data
        }, status=status.HTTP_200_OK)