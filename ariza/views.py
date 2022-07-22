from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ArizaSerializer
from .models import *


class ArizaApiCreateView(generics.CreateAPIView):
    serializer_class = ArizaSerializer
    queryset = Ariza.objects.all()



ariza_create_view = ArizaApiCreateView.as_view()
