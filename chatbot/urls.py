from chatbot import views
from django.urls import path


urlpatterns = [
    path('new/', views.start_chat, name='start_new_chat'),
    path('history/', views.get_user_chat_history, name='get_user_chat_history'),
    path('session/<str:session_id>/', views.get_chat_session, name='get_chat_session'),
    path('<str:session_id>/', views.continue_chat, name='continue_chat'),
    path('<str:session_id>/delete/', views.delete_chat_session, name='delete_chat_session'),
]