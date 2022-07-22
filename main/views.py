from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from .models import *
from .serializers import *
from ariza.serializers import ArizaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ArizaFilter, StudentFilter
class UniversityApiView(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class StudentApiView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['fish']
    filterset_class = StudentFilter
    # filterset_fields = ['', 'amount', 'created_at']

class HomiyApiView(viewsets.ModelViewSet):
    queryset = Homiy.objects.all()
    serializer_class = HomiySerializer


class ArizaApiView(viewsets.ModelViewSet):
    queryset = Ariza.objects.all()
    serializer_class = ArizaSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['fish', 'tashkilot']
    http_method_names = ['get', "update", "delete",'put', 'head', 'options']
    filterset_class = ArizaFilter
    # filterset_fields = ['status', 'amount','created_at']



