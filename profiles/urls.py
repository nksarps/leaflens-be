from django.urls import path
from profiles import views

urlpatterns = [
    path('me/', views.view_profile, name='view_profile'),
    path('update/me/', views.update_profile_info, name='update_profile_info'),
]