from ariza.models import *
from django.db.models import Q
from django.db.models import Sum
from django.db import models
from django.core.exceptions import ValidationError

class University(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StudentTturi(models.TextChoices):
    bakalavr = "bakalavr"
    magistr = "magistr"


class Student(models.Model):
    otm = models.ForeignKey(University, models.SET_NULL, null=True, verbose_name="Talabaning universiteti", )
    fish = models.CharField(max_length=255, verbose_name="Familya ism sharifi")
    phone = models.CharField(max_length=25, verbose_name="Talabani telefon raqami")
    t_turi = models.CharField(max_length=25, choices=StudentTturi.choices, verbose_name="Talabaning turi")
    kontrakt = models.BigIntegerField(verbose_name="Talaba kontrakti")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self, exclude=None):
        all_paid = Homiy.objects.filter(student=self).aggregate(Sum('amount'))
        if self.kontrakt<all_paid['amount__sum']:
            raise ValidationError({"kontrakt": [f"Ushbu talabaga allaqachon {all_paid['amount__sum']} miqdorida homiylik qilingan studentni kontrakt summasini bundan kamaytira olmaysiz"]})
        super(Student, self).clean()
    def save(self,*args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.fish


class Homiy(models.Model):
    homiy = models.ForeignKey(Ariza, models.CASCADE, verbose_name="Homiylar")
    student = models.ForeignKey(Student, models.CASCADE, verbose_name="Talabalar")
    amount = models.BigIntegerField(verbose_name="Homiylik miqdori")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def all_homiy_amount(self):
        if self.id:
            jami_homiylik = Homiy.objects.filter(Q(homiy=self.homiy) & ~Q(id=self.id)).aggregate(
                Sum('amount'))
        else:
            jami_homiylik = Homiy.objects.filter(homiy=self.homiy).aggregate(Sum('amount'))
        print(jami_homiylik)
        if jami_homiylik['amount__sum']:
            jami_homiylik = jami_homiylik['amount__sum']
        else:
            jami_homiylik = 0
        jami_homiylik+=self.amount
        return jami_homiylik

    @property
    def all_paid_kontrakt(self):
        if self.id:
            paid_kontrakt = Homiy.objects.filter(Q(student=self.student) & ~Q(id=self.id)).aggregate(
                Sum('amount'))
        else:
            paid_kontrakt = Homiy.objects.filter(Q(student=self.student)).aggregate(Sum('amount'))
        if paid_kontrakt['amount__sum']:
            paid_kontrakt = paid_kontrakt['amount__sum']
        else:
            paid_kontrakt = 0
        paid_kontrakt+=self.amount
        return paid_kontrakt

    def clean(self, exclude=None):
        if self.homiy.status == ArizaStatus.yangi or self.homiy.paymentType == PaymentOptions.none:
            raise ValidationError(
                {"homiy": "homiy homiylik qilishi uchun avval tasdiqlanishi va to'lov turi ko'rsatilishi kerak"})
        if self.all_homiy_amount > self.homiy.amount:
            maximum = self.homiy.amount - self.all_homiy_amount + self.amount
            if maximum>0:
                message = f"Homiy maximum {self.homiy.amount - self.all_homiy_amount + self.amount} miqdorida homiylik qila oladi"
            else:
                message = "Ushbu homiy barcha mablag'ini homiylik qilib bo'lgan"
            raise ValidationError({"amount":message})

        if self.all_paid_kontrakt > self.student.kontrakt:
            max_kontrakt = self.student.kontrakt - self.all_paid_kontrakt + self.amount
            if max_kontrakt>0:
                message = "Jami homiyliklar miqdori Studentni kontrakt summasidan oshib ketdi\n\n"
                f"Maxium {self.student.kontrakt - self.all_paid_kontrakt + self.amount} so'm"
            else:
                message = "Talabaning kontrakti allaqachon to'liq to'langan"
            raise ValidationError({"amount": message})
        super().clean()
    def save(self, *arg, **kwargs):
        self.clean()
        super().save(*arg, **kwargs)

    def __str__(self):
        return f"{self.homiy.fish}      {self.student.fish}"
