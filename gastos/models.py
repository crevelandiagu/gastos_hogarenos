from django.db import models


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    balance = models.FloatField(null=True, blank=True, default=False)

    def __str__(self):
        return {"name": self.name,
                "balance": self.balance,
                }


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField(null=True, blank=True, default=None)
    description = models.CharField(max_length=250)
    income = models.BooleanField(null=True, blank=True, default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return {self.title
                }
