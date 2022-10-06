import json
from faker import Faker
from django.test import TestCase
from gastos.models import Account
from gastos.models import Transaction
from django.test import Client

class TestDetailAccount(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data_factory = Faker()
        cls.account = {
            "name": cls.data_factory.name(),
            "balance": cls.data_factory.random_int(100, 200)
        }

    def test_list_detail_account(self):
        create_account_1 = Account(
            name=self.account['name'],
            balance=self.account['balance']
        )
        create_account_1.save()
        transaction_1 = {
            'amount': self.data_factory.pyfloat(),
            'description': self.data_factory.name(),
            'income': True,
            'id': 1
           }

        create_transaction_1 = Transaction(
            amount=transaction_1['amount'],
            description=transaction_1['description'],
            income=transaction_1['income'],
            accounts_id=1

        )
        create_transaction_1.save()


        response = Client().get('/api/detalle_cuenta/1')
        respon = json.loads(response.content)['detail_transaction']
        respon[0].pop('created_at')
        self.assertEqual(transaction_1, respon[0])

