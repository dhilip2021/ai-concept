
from django.urls import path
from .views import *
urlpatterns = [
   path('', jarvas_view, name='jarvas'),
]
