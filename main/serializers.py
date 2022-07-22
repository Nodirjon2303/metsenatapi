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

    def update(self, instance, validated_data):
        paid = sum([i.amount for i in Homiy.objects.filter(student=instance)])
        if paid > validated_data.get('kontrakt'):
            raise serializers.ValidationError({'kontrakt': f"Already {paid} is paid for student kontrakt "})
        return super().update(instance, validated_data)

    def get_homiylar(self, obj):
        homiylar = Homiy.objects.filter(student=obj)
        return HomiySerializer(homiylar, many=True, context=self.context).data

    def get_created_date(self, obj):
        date = obj.created_at.strftime("%d.%m.%Y")
        return date

    def get_paid(self, obj):
        paid = sum([i.amount for i in Homiy.objects.filter(student=obj)])
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

    def update(self, instance, validated_data):
        print(validated_data)
        paid = sum([i.amount for i in Homiy.objects.filter(student=validated_data.get('student'))]) - instance.amount
        if paid + self.validated_data.get('amount') > instance.student.kontrakt:
            raise serializers.ValidationError(
                {"status": f"error Summa talabani kontaktidan oshib ketdi",
                 "maximum": instance.student.kontrakt - paid})
        all_spent = sum([i.amount for i in Homiy.objects.filter(homiy=validated_data.get('homiy'))]) - instance.amount
        if all_spent + validated_data.get('amount') > instance.homiy.amount:
            raise serializers.ValidationError(
                {"status": f"error amount homiyning mablag'idan oshib ketdi",
                 "maximum": instance.homiy.amount - all_spent})
        homiy = validated_data.get('homiy')
        if homiy.status != 'tasdiqlangan':
            raise serializers.ValidationError({"status": " error Homiy hali tasdiqlanmagan"})
        return super().update(instance, validated_data)

    def create(self, validated_data):
        homiy = validated_data.get("homiy")
        student = validated_data.get('student')
        amount = validated_data.get('amount')
        all_spent = sum([i.amount for i in Homiy.objects.filter(homiy=homiy)])
        if all_spent + amount > homiy.amount:
            raise serializers.ValidationError(
                {"status": f"error amount homiyning mablag'idan oshib ketdi",
                 "maximum": homiy.amount - all_spent})
        paid = sum([i.amount for i in Homiy.objects.filter(student=validated_data.get('student'))])
        if paid + self.validated_data.get('amount') > student.kontrakt:
            raise serializers.ValidationError(
                {"status": f"error Summa talabani kontaktidan oshib ketdi",
                 "maximum": student.kontrakt - paid})
        if homiy.status != 'tasdiqlangan':
            raise serializers.ValidationError({"status": " error Homiy hali tasdiqlanmagan"})

        return super(HomiySerializer, self).create(validated_data)
