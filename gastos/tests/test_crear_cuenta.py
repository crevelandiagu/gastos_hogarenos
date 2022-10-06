import json
from faker import Faker
from django.test import TestCase
from gastos.models import Account
from django.test import Client

class TestAccount(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data_factory = Faker()
        cls.account = {
            "name": cls.data_factory.name(),
            "balance": cls.data_factory.random_int(100, 200)
        }

    def test_create_account(self):
        create_account = Account(
            name=self.account['name'],
            balance=self.account['balance']
        )
        create_account.save()
        new_account = Account.objects.get(id=1)
        self.assertEqual(new_account.name, self.account['name'])
        self.assertEqual(new_account.balance, self.account['balance'])

    def test_list_account(self):
        create_account_1 = Account(
            name=self.account['name'],
            balance=self.account['balance']
        )
        create_account_1.save()
        create_account_2 = Account(
            name=self.account['name'],
            balance=self.account['balance']
        )
        create_account_2.save()
        response = Client().get('/api/cuenta/')
        respon = json.loads(response.content)
        self.assertIn(self.account, respon)
