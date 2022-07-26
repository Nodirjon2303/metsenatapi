from .models import *

from rest_framework import serializers
from ariza.validators import validate_phone_number
from ariza.serializers import ArizaSerializer


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = [
            'pk',
            'name'
        ]


class ArizaPublicSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    fish = serializers.CharField(read_only=True, max_length=255)
    phone = serializers.CharField(max_length=15, read_only=True)
    type = serializers.CharField(max_length=25, read_only=True)
    tashkilot = serializers.CharField(read_only=True)
    amount = serializers.IntegerField(read_only=True)
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='ariza-detail',
        lookup_field='pk',
        read_only=True
    )


class StudentPublicSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='student-detail',
        lookup_field='pk',
        read_only=True
    )
    fish = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    kontrakt = serializers.CharField(read_only=True)


class StudentSerializer(serializers.ModelSerializer):
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='student-detail',
        lookup_field='pk',
        read_only=True
    )
    paid = serializers.SerializerMethodField(read_only=True)
    homiylar = serializers.SerializerMethodField(read_only=True)
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
            'paid',
            'kontrakt',
            'homiylar',
            'created_date',
        ]



    def get_homiylar(self, obj):
        homiylar = Homiy.objects.filter(student=obj)
        return HomiySerializer(homiylar, many=True, context=self.context).data

    def get_created_date(self, obj):
        date = obj.created_at.strftime("%d.%m.%Y")
        return date

    def get_paid(self, obj):
        paid = Homiy.objects.filter(student=obj).aggregate(Sum('amount')).get('amount__sum')
        return paid


class HomiySerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField(read_only=True)
    homiy_data = serializers.SerializerMethodField(read_only=True)
    student_data = StudentPublicSerializer(source='student', read_only=True)
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='homiy-detail',
        lookup_field='pk',
        read_only=True
    )

    class Meta:
        model = Homiy
        fields = [
            'pk',
            'edit_url',
            'amount',
            'created_date',
            'homiy',
            'student',
            'homiy_data',
            'student_data'
        ]

    def get_created_date(self, obj):
        return obj.created_at.strftime("%d.%m.%Y")

    def get_homiy_data(self, obj):
        homiy = ArizaPublicSerializer(read_only=True, instance=obj.homiy,
                                      context={'request': self.context.get('request')}).data
        return homiy

    
    


