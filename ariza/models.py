from django.db import models


class Ariza(models.Model):
    type_options = (('yuridik', "Yuridik shaxs"), ('jismoniy', "Jismoniy shaxs"))
    type = models.CharField(max_length=255, choices=type_options)
    status_options = (
        ('yangi', "Yangi ariza tashlandi"),
        ('moderatsiya', "Moderatsya jarayonida"),
        ('tasdiqlangan', "Tasdiqlangan"),
        ('cancel', "Bekor qilingan")
    )
    payment_type_options = (
        ("exchange", "Pul O'tqazmalari"),
        ("cash", "Naqt to'lov"),
        ("None", "None")
    )
    fish = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    amount = models.BigIntegerField()
    tashkilot = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=125, default='yangi', choices=status_options)
    paymentType = models.CharField(max_length=35, choices=payment_type_options, default='None')

    def option_status(self):
        return [i[0] for i in self.status_options]


    def  save(self, *args, **kwargs):
        if not self.id:
            self.status = self.status_options[0][0]
            self.paymentType = self.payment_type_options[0][0]
        if self.type not in [i[0] for i in self.type_options]:
            if self.tashkilot:
                self.type = self.type_options[0][0]
            else:
                self.type = self.type_options[1][0]
        if self.status not in self.option_status():
            self.status = self.option_status()[0]
        if self.paymentType not in [i[0] for i in self.payment_type_options]:
            self.paymentType = self.payment_type_options[0][0]

        if self.type == 'jismoniy':
            self.tashkilot = ''
        elif not self.tashkilot:
            raise ValueError("type=yuridik tashkilot is required")

        
        super(Ariza, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.type}   {self.amount}  {self.status}"
