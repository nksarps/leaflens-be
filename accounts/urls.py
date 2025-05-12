from accounts import views
from django.urls import path

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name='log_in'),
]