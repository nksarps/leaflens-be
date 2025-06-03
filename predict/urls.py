from django.urls import path
from predict import views


urlpatterns = [
    path('', views.predict_disease, name='predict_disease'),
    path('all/', views.get_all_predictions, name='get_all_predictions')
]