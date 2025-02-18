from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path('', index, name='home'),
    path('weather/<str:city_name>/', index, name='city_weather'),
    path('delete/<str:city_name>/', views.delete_city, name='delete_city')

]
