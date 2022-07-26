from rest_framework import serializers
from .models import Ariza
from main.models import Homiy
from rest_framework.reverse import reverse
from .validators import *
from django.db.models import Sum

class ArizaSerializer(serializers.ModelSerializer):
    spent = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='ariza-detail',
        lookup_field='pk',
    )
    phone = serializers.CharField(max_length=13, validators=[
        validate_phone_number
    ])
    class Meta:
        model = Ariza
        fields = [
            'pk',
            'edit_url',
            'fish',
            'phone',
            'amount',
            'spent',
            'type',
            'tashkilot',
            'status',
            'created_date',
            'paymentType'
        ]

    def get_spent(self, obj):
        spent = Homiy.objects.filter(homiy=obj).aggregate(Sum('amount')).get("amount__sum")
        return spent


    def get_created_date(self, obj):
        date = obj.created_at.strftime("%d.%m.%Y")
        return date


