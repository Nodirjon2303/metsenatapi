from itertools import chain

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
from django.db.models import Sum, Count, Avg


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
        arizalar = Ariza.objects.values('created_at__date', 'created_at__month').annotate(homiy_soni=Count('id'))
        studentlar = Student.objects.values('created_at__date', 'created_at__month').annotate(student_soni=Count('id'))
        # print(arizalar, studentlar)
        # print(list(chain(arizalar, studentlar)))
        # arizalar = Ariza.objects.all().extra(
        #     select={"student":'main_student.id'},
        #     tables=['main_student']
        # )
        # """
        # Select sum(student.id), sum(ariza.id) , ariza.created_at__date
        # from ariza,
        # FULL OUTER JOIN student
        # on student.created_at__date =ariza.created_at__date
        # """

        # start_date = datetime.datetime(year=today.year, month=1, day=1)
        # month = []
        # while start_date <= today:
        #     homiy_day = Ariza.objects.filter(created_at__day=start_date.day, created_at__month=start_date.month,
        #                                      created_at__year=start_date.year).count()
        #     student_day = Student.objects.filter(created_at__day=start_date.day, created_at__month=start_date.month,
        #                                          created_at__year=start_date.year).count()
        #     month.append({
        #         'day': start_date.day,
        #         'homiy': homiy_day,
        #         'student': student_day
        #     })
        #     if start_date.month != (start_date + datetime.timedelta(days=1)).month:
        #         data.append({
        #             'name': month_names[start_date.month],
        #             'days': month,
        #             'homiy': Ariza.objects.filter(created_at__gte=(start_date - datetime.timedelta(days=len(month))),
        #                                           created_at__lte=start_date).count(),
        #             'student': Student.objects.filter(
        #                 created_at__gte=(start_date - datetime.timedelta(days=len(month))), created_at__lte=start_date).count(),
        print(arizalar, studentlar)
        #         })
        #         month = []
        #     start_date += datetime.timedelta(days=1)
        # if month:
        #     data.append({
        #         'name': month_names[start_date.month],
        #         'days': month,
        #         'homiy': Ariza.objects.filter(created_at__gte=(start_date - datetime.timedelta(days=len(month))),
        #                                       created_at__lte=start_date).count(),
        #         'student': Student.objects.filter(created_at__gte=(start_date - datetime.timedelta(days=len(month))),
        #                                           created_at__lte=start_date).count(),
        #     })
        response_data = {
            "all_paid": Homiy.objects.all().aggregate(Sum('amount')).get('amount__sum'),
            'all_asked': Student.objects.all().aggregate(Sum('kontrakt')).get('kontrakt__sum'),
            'must_pay': -   Homiy.objects.all().aggregate(Sum('amount')).get(
                'amount__sum') + Student.objects.all().aggregate(Sum('kontrakt')).get('kontrakt__sum'),
            # 'homiy': Ariza.objects.filter(created_at__lte=today).count(),
            # 'student': Student.objects.filter(created_at__lte=today).count(),
            'monthly': data
        }
        return Response(response_data, status=status.HTTP_200_OK)
