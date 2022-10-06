import json
from faker import Faker
from django.test import TestCase
from gastos.models import Account
from gastos.models import Transaction
from django.test import Client

class TestTransaction(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data_factory = Faker()
        cls.client = Client()


    def test_create_transaction(self):

        cuenta = {
            "balance": 10,
            "name": "ff"
        }

        self.client.post('/crear_cuenta/',
                         json.dumps(cuenta),
                         content_type="application/json")

        transaction = {

            "amount": self.data_factory.pyfloat(),
            "description": self.data_factory.name(),
            "income": True,

        }
        response = self.client.post('/transacion/1',
                                    json.dumps(transaction),
                                    content_type="application/json")

        # self.assertEqual(response, 200)


    def test_delete_transaction(self):
        create_account = Account(
            name=self.data_factory.name(),
            balance=self.data_factory.random_int(100, 200)
        )
        create_account.save()

        create_transaction = Transaction(
            amount=self.data_factory.random_int(100, 200),
            description=self.data_factory.name(),
            income=True,
            accounts_id=1
        )
        create_transaction.save()

        transaction = {
            "id": 1
        }
        response = self.client.delete('/transacion/1',
                                    json.dumps(transaction),
                                    content_type="application/json")

        # self.assertEqual(response.status_code, 200)
