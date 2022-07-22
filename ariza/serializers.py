from rest_framework import serializers
from .models import Ariza
from main.models import Homiy
from rest_framework.reverse import reverse
from .validators import *

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
        spent = sum([i.amount for i in Homiy.objects.filter(homiy=obj)])
        return spent

    def create(self, validated_data):
        type = validated_data.get('type')
        tashkilot = validated_data.get('tashkilot')
        if type == 'yuridik' and not tashkilot:
            raise serializers.ValidationError({"tashkilot": "tashkilot is required for yuridik user"})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        print(validated_data, instance)
        all_spent = sum([i.amount for i in Homiy.objects.filter(homiy=instance)])
        if all_spent > validated_data.get('amount'):
            raise serializers.ValidationError({"amount": f"already {all_spent} sum spent"})
        if all_spent > 0 and validated_data.get('status') != 'tasdiqlangan':
            raise serializers.ValidationError({"status": "status must be tasdiqlangan in this user who  spent money"})
        return super().update(instance, validated_data)

    def get_created_date(self, obj):
        date = obj.created_at.strftime("%d.%m.%Y")
        return date

