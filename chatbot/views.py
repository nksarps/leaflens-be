import os, uuid
import google.generativeai as genai
from accounts.permissions import IsVerified
from chatbot.models import Chat
from chatbot.serializers import SessionSerializer
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

@api_view(['POST'])
@permission_classes([IsVerified])
def start_chat(request):
    if request.method == 'POST':
        user = request.user

        user_message = request.data.get('message')

        if not user_message:
            return Response({
                'success':False,
                'message':'Message is required to start chat'
            }, status=status.HTTP_400_BAD_REQUEST)

        session_id = str(uuid.uuid4())

        try:
            chat = model.start_chat()

            response = chat.send_message(user_message)
            bot_response = response.text

            Chat.objects.create(
                user=user,
                session_id=session_id,
                sender='user',
                message=user_message
            )

            Chat.objects.create(
                user=user,
                session_id=session_id,
                sender='model',
                message=bot_response
            )

            return Response({
                'success':True,
                'session_id':session_id,
                'response':bot_response
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error processing chat: {e}")
            return Response({
                'success':False,
                'message':f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsVerified])
def continue_chat(request, session_id:str):
    if request.method == 'POST':
        user = request.user

        if not Chat.objects.filter(session_id=session_id, user=user).exists():
            return Response({
                'success':False,
                'message':'Session ID not found. Start a new chat.'
            }, status=status.HTTP_404_NOT_FOUND)

        user_message = request.data.get('message')

        if not user_message:
            return Response({
                'success':False,
                'message':'Message is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            chat_history_db = Chat.objects.filter(session_id=session_id)

            history_for_gemini = []
            for msg in chat_history_db:
                role = 'user' if msg.sender == 'user' else 'model'
                history_for_gemini.append({'role':role, 'parts':[msg.message]})

            chat = model.start_chat(history=history_for_gemini)

            response = chat.send_message(user_message)
            bot_response = response.text

            Chat.objects.create(
                user=user,
                session_id=session_id,
                sender='user',
                message=user_message
            )

            Chat.objects.create(
                user=user,
                session_id=session_id,
                sender='model',
                message=bot_response
            )

            return Response({
                'success':True,
                'session_id':session_id,
                'response':bot_response
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Error processing chat: {e}")
            return Response({
                'success':False,
                'message':f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
@api_view(['GET'])
@permission_classes([IsVerified])
def get_user_chat_history(request):
    user = request.user

    user_messages = Chat.objects.filter(user=user).order_by('session_id', 'timestamp')

    grouped_messages = {}
    session_latest_timestamps = {}

    for message in user_messages:
        if message.session_id not in grouped_messages:
            grouped_messages[message.session_id] = []
        
        grouped_messages[message.session_id].append(message)
        
        session_latest_timestamps[message.session_id] = message.timestamp

    sorted_session_ids = sorted(
        session_latest_timestamps.items(), 
        key=lambda item: item[1], 
        reverse=True 
    )

    serialized_data = []
    for session_id, _ in sorted_session_ids:
        messages_list = grouped_messages[session_id]

        serialized_data.append({
            'session_id': session_id,
            'messages': messages_list
        })
    
    serializer = SessionSerializer(serialized_data, many=True)

    return Response({
        'success': True,
        'messages': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsVerified])
def delete_chat_session(request, session_id: str):
    user = request.user

    chats = Chat.objects.filter(session_id=session_id, user=user)
    
    if not chats.exists():
        return Response({
            'success': False,
            'message': 'Session does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    
    count, _ = chats.delete()

    return Response({
        'success': True,
        'message': f'{count} chat(s) successfully deleted'
    }, status=status.HTTP_200_OK)