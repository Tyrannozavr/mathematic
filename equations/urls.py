from django.urls import path
from .views import equations

urlpatterns = [
    path('', equations, name='equations'),
]