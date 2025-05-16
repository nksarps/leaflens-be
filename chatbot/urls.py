from chatbot import views
from django.urls import path


urlpatterns = [
    path('new/', views.start_chat, name='start_new_chat'),
    path('<str:session_id>/', views.continue_chat, name='continue_chat')
]