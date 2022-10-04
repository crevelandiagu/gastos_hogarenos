from rest_framework import serializers
from gastos.models import Account
from gastos.models import Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'balance')


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'description', 'income', 'created_at')


class AccountDetailSerializer(serializers.ModelSerializer):
    detail_acount = AccountSerializer()
    detail_transaction = TransactionDetailSerializer(many=True)

    class Meta:
        model = Account
        fields = ('detail_acount', 'detail_transaction')

