from accounts import views
from django.urls import path

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name='log_in'),
    path('verify-user/', views.verify_user, name='verify_user'),
    path('update-info/', views.update_user_info, name='update_user_info'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset-confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('user/', views.get_current_user, name='get_current_user')
]