from django.urls import path
from predict import views


urlpatterns = [
    path('', views.predict_disease, name='predict_disease')
]