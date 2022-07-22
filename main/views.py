from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from .models import *
from .serializers import *
from ariza.serializers import ArizaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ArizaFilter, StudentFilter
from rest_framework import generics
import datetime
from django.utils import timezone
import pytz


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
    http_method_names = ['get', "update", "delete", 'put', 'head', 'options']
    filterset_class = ArizaFilter
    # filterset_fields = ['status', 'amount','created_at']


class DashboardView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        month_names = {
            1: "Yanvar",
            2: "Fevral",
            3: "Mart",
            4: "Aprel",
            5: "May",
            6: "Iyun",
            7: "Iyul",
            8: "Avgust",
            9: "Sentabr",
            10: "Oktabr",
            11: "Noyabr",
            12: "Dekabr"
        }
        data = []
        today = datetime.datetime.today()
        start_date = datetime.datetime(year=today.year, month=1, day=1)
        month = []
        while start_date <= today:
            homiy_day = Ariza.objects.filter(created_at__lte=start_date).count()
            student_day = Student.objects.filter(created_at__lte=start_date).count()
            month.append({
                'day': start_date.day,
                'homiy': homiy_day,
                'student': student_day
            })
            if start_date.month != (start_date + datetime.timedelta(days=1)).month:
                data.append({
                    'name': month_names[start_date.month],
                    'days': month,
                    'homiy': month[-1]['homiy'],
                    'student': month[-1]['student']
                })
                month = []
            start_date+=datetime.timedelta(days=1)
        if month:
            data.append({
                'name': month_names[start_date.month],
                'days': month,
                'homiy': month[-1]['homiy'],
                'student': month[-1]['student']
            })
        response_data = {
            "all_paid": sum([i.amount for i in Homiy.objects.all()]),
            'all_asked': sum([i.kontrakt for i in Student.objects.all()]),
            'must_pay': sum([i.amount for i in Homiy.objects.all()]) - sum([i.kontrakt for i in Student.objects.all()]),
            'homiy': Ariza.objects.filter(created_at__lt=today).count(),
            'student': Student.objects.filter(created_at__lte=today).count(),
            'monthly': data
        }
        return Response(response_data, status=status.HTTP_200_OK)
