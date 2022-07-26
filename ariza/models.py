from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.apps import apps


class ArizaStatus(models.TextChoices):
    yangi = "yangi"
    moderatsiya = 'moderatsiya'
    tasdiqlangan = 'tasdiqlangan'
    cancel = 'cancel'


class PaymentOptions(models.TextChoices):
    cash = 'cash'
    exchange = 'exchange'
    none = "None"


class ArizaType(models.TextChoices):
    yuridik = "yuridik"
    jismoniy = 'jismoniy'


class Ariza(models.Model):
    type = models.CharField("Arizaning turi", max_length=255, choices=ArizaType.choices)
    fish = models.CharField("Ism Familya", max_length=255)
    phone = models.CharField("Telefon raqam", max_length=25)
    amount = models.BigIntegerField("Homiylik miqdori")
    tashkilot = models.CharField("Tashkilot nomi", max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField("Ariza holati", max_length=125, default='yangi', choices=ArizaStatus.choices)
    paymentType = models.CharField("To'lov turi", max_length=35, choices=PaymentOptions.choices,
                                   default=PaymentOptions.none)

    def clean(self):
        if not self.id:
            self.status = ArizaStatus.yangi
            self.paymentType = PaymentOptions.none
        if self.type == ArizaType.jismoniy:
            self.tashkilot = ''

        if self.type == ArizaType.yuridik and not self.tashkilot:
            raise ValidationError({'tashkilot': ["Tashkilot is required", ]})
        if self.paymentType == PaymentOptions.none and self.status == ArizaStatus.tasdiqlangan:
            raise ValidationError({'paymentType': ["Userni tasdiqlash uchun avval to'lov turini tanlang"]})
        Homiy = apps.get_model('main.Homiy')
        if self.id and self.paymentType != PaymentOptions.none and self.status != ArizaStatus.yangi:
            allhomiylik = Homiy.objects.filter(homiy=self).aggregate(Sum("amount"))
            print(allhomiylik)
            if allhomiylik['amount__sum'] > self.amount:
                raise ValidationError(
                    {'amount': [f"Ushbu homiy allaqachon {allhomiylik['amount__sum']} so'm homiylikni sarflab bo'ldi"]})
            if allhomiylik['amount__sum']:
                if self.status != ArizaStatus.tasdiqlangan:
                    raise ValidationError(
                        {'status': [
                            f"Ushbu homiy allaqachon talabalarga homiylik qilgan. Homiyning statusini  o'zgartirish uchun avval homiyning homiylikalarini o'chirishingiz kerak"]})

    def save(self, *args, **kwargs):
        self.clean()
        super(Ariza, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.fish}  {self.type}   {self.amount}  {self.status}"
