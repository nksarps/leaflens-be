from django.urls import path
from predict import views


urlpatterns = [
    path('', views.predict_disease, name='predict_disease'),
    path('all/', views.get_all_predictions, name='get_all_predictions'),
    path('<str:id>/', views.get_prediction, name='get_prediction'),
    path('<str:id>/delete/', views.delete_prediction, name='delete_prediction'),
]