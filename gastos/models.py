from django.db import models
from datetime import datetime


class Base(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        default=datetime.now,
        blank=True
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class Account(Base):

    name = models.CharField(max_length=250)
    balance = models.FloatField(null=True, blank=True, default=False)

    def __str__(self):
        return {"name": self.name,
                "balance": self.balance,
                }


class Transaction(Base):

    amount = models.FloatField(null=True, blank=True, default=None)
    description = models.CharField(max_length=250)
    income = models.BooleanField(null=True, blank=True, default=False)
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE)

