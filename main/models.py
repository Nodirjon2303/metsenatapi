from django.db import models
from ariza.models import Ariza
from django.db.models import Q


class University(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    t_turi_choices = (
        ("bakalavr", "Bakalavr daraja"),
        ('magistr', "Magistratura talabasi")
    )
    otm = models.ForeignKey(University, models.SET_NULL, null=True)
    fish = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    t_turi = models.CharField(max_length=25, choices=t_turi_choices)
    kontrakt = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.t_turi not in [i[0] for i in self.t_turi_choices]:
            error = "t_turi field must be in " + str([i[0] for i in self.t_turi_choices])
            raise ValueError(error)
        else:
            super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.fish


class Homiy(models.Model):
    homiy = models.ForeignKey(Ariza, models.CASCADE)
    student = models.ForeignKey(Student, models.CASCADE)
    amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.homiy.status != "tasdiqlangan" or self.homiy.paymentType == 'None':
            raise ValueError("homiy homiylik qilishi uchun avval tasdiqlanishi va to'lov turi ko'rsatilishi kerak")
        if self.id:
            # hozirgi homiylikda bilan  homiyni barcha qilgan homiyliklari qilmoqchi bo'layotgani
            jami_homiylik = sum([i.amount for i in Homiy.objects.filter(Q(homiy=self.homiy) & ~Q(id=self.id))]) + self.amount


            # hozirgi homiylik bilan shu studentga qancha homiylik qilinganayotgani
            jami_student_homiy_amount = sum(
                [i.amount for i in Homiy.objects.filter(Q(student=self.student) & ~Q(id=self.id))]) + self.amount
        else:
            jami_homiylik = sum([i.amount for i in Homiy.objects.filter(homiy=self.homiy)]) + self.amount

            jami_student_homiy_amount = sum(
                [i.amount for i in Homiy.objects.filter(Q(student=self.student))]) + self.amount

        if jami_homiylik > self.homiy.amount:
            raise ValueError(
                f"Homiy maximum {self.homiy.amount - jami_homiylik + self.amount} miqdorida homiylik qila oladi")

        if jami_student_homiy_amount > self.student.kontrakt:
            raise ValueError("Jami homiyliklar miqdori Studentni kontrakt summasidan oshib ketdi\n\n"
                             f"Maxium {self.student.kontrakt - jami_student_homiy_amount + self.amount} so'm")
        return super(Homiy, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.homiy.fish}      {self.student.fish}"
