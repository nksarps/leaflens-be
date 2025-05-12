from accounts.serializers import SignUpSerializer, LogInSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def sign_up(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({
                'success':True,
                'user':serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success':False,
            'message':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


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