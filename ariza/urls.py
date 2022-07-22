from django.urls import path
from .views import *

urlpatterns = [
    path('', ariza_create_view, name='ariza')
]