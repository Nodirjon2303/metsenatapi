import django_filters
from django_filters import rest_framework as filters
from .models import Ariza, Student
from django.forms import  DateInput


class ArizaFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name='created_at', lookup_expr='gte',
                                   widget=DateInput(format='%d-%m-%Y', attrs={"type":'date'})
                                   )
    to_date = filters.DateFilter(field_name='created_at', lookup_expr='lte',
                                   widget=DateInput(format='%d-%m-%Y', attrs={"type": 'date'})
                                   )
    class Meta:
        model = Ariza
        fields = ['status', 'amount', 'from_date', 'to_date']
class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = ['t_turi', 'otm']

