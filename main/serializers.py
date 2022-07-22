from .models import *

from rest_framework import serializers
from ariza.validators import validate_phone_number


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='student-detail',
        lookup_field='pk',
    )
    spent = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    phone = serializers.CharField(max_length=13, validators=[
        validate_phone_number
    ])

    class Meta:
        model = Student

        fields = [
            'pk',
            'edit_url',
            'fish',
            'phone',
            'otm',
            't_turi',
            'spent',
            'kontrakt',
            'created_date',

        ]

    def get_created_date(self, obj):
        date = obj.created_at.strftime("%d.%m.%Y")
        return date

    def get_spent(self, obj):
        spent = sum([i.amount for i in Homiy.objects.filter(student=obj)])
        return spent


class HomiySerializer(serializers.ModelSerializer):
    class Meta:
        model = Homiy
        fields = '__all__'
