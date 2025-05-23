from accounts.permissions import IsVerified
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsVerified])
def view_profile(request):
    if request.method == 'GET':
        user = request.user

        profile = Profile.objects.get(user=user)
        if not profile:
            return Response({
                'success':False,
                'message':'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile)

        return Response({
            'success':True,
            'message':serializer.data
        }, status=status.HTTP_200_OK)
    

@api_view(['PUT', 'PATCH'])
@permission_classes([IsVerified])
def update_profile_info(request):
    if request.method == 'PUT' or request.method == 'PATCH':
        user = request.user

        profile = Profile.objects.get(user=user)
        if not profile:
            return Response({
                'success':False,
                'message':'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'success':True,
                'message':'Profile updated',
                'profile':serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success':False,
            'message':serializer.data
        }, status=status.HTTP_400_BAD_REQUEST)
