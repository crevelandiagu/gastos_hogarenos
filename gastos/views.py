import os
import json
from datetime import datetime, timedelta

from .models import Account
from .models import Transaction
from .querysets import crear_transaccion

from .serializers import AccountSerializer
from .serializers import AccountDetailSerializer
from .serializers import TransactionSerializer
from .serializers import TransactionDeleteSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import F

class Health(APIView):
    """Check avaiability"""

    def get(self, request):
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class AccountView(APIView):

    def post(self, request, id_acount=None):
        """
        Creates new acount
        """
        serializer = AccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "code": 400,
                    "message": "The request is not valid",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        create_account = Account(
            name=serializer.data['name'],
            balance=serializer.data['balance']
        )
        create_account.save()

        keyword = {
            "amount": serializer.data['balance'],
            "description": "balance inicia",
            "income": True,
            "accounts_id": create_account.id
        }
        crear_transaccion(**keyword)

        return Response(
            {
                "success": True,
                "code": 200,
                "account": serializer.data,

            },
            status=status.HTTP_200_OK
        )

    def get(self, request, id_acount=None):
        """
        get acount's
        """
        documents = Account.objects.all()
        serializer = AccountSerializer(documents, many=True)
        return Response(serializer.data)

    def put(self, request, id_acount):
        serializer = AccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "code": 400,
                    "message": "The request is not valid",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        Account.objects.filter(id=id_acount).update(balance=serializer.data['balance'])

        keyword = {
            "amount": serializer.data['balance'],
            "description": "ajuste manual",
            "income": True,
            "accounts_id": id_acount
        }
        crear_transaccion(**keyword)

        return Response(
            {
                "success": True,
                "code": 200,
                "account": id_acount,
            },
            status=status.HTTP_200_OK
        )


class AccountDetailView(APIView):

    def detail_date(self, date, id):


        data = date.split('-')
        if len(data) != 3:
            return Response(
                {
                    "success": False,
                    "code": 400,
                    "message": "The request is not valid",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        anio = int(data[0])
        mes = int(data[1])
        print('a')
        start_date = datetime(anio, mes, 1).strftime("%Y-%m-%d")
        end_date = (datetime(anio + int(mes / 12), mes % 12 + 1, 1) + timedelta(days=-1)).strftime("%Y-%m-%d")

        detail_acount = Account.objects.get(id=id)
        detail_transaction = Transaction.objects.filter(accounts__id=id, created_at__range=(start_date, end_date)).order_by('-created_at')
        obj = {'detail_acount': detail_acount, 'detail_transaction': detail_transaction}
        serializer = AccountDetailSerializer(obj)

        return Response(serializer.data)

    def get(self, request, id, date=None):
        """
        get details acount's
        """
        if date:

            return self.detail_date(date, id)

        detail_acount = Account.objects.get(id=id)
        detail_transaction = Transaction.objects.filter(accounts__id=id).order_by('-created_at')
        obj = {'detail_acount': detail_acount, 'detail_transaction': detail_transaction}
        serializer = AccountDetailSerializer(obj)
        return Response(serializer.data)


class TransactionView(APIView):

    def post(self, request, id_acount):
        """
        Creates new acount
        """
        serializer = TransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "code": 400,
                    "message": "The request is not valid",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        keyword = {
            "amount": serializer.data['amount'],
            "description": serializer.data['description'],
            "income": serializer.data['income'],
            "accounts_id": id_acount
        }
        crear_transaccion(**keyword)

        acount_user = Account.objects.get(id=id_acount)
        new_balance = acount_user.balance + serializer.data['amount']\
            if serializer.data['income'] is True else acount_user.balance - serializer.data['amount']

        Account.objects.filter(id=id_acount).update(balance=new_balance)
        return Response(
            {
                "success": True,
                "code": 200,
                "transaction": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, id_acount):
        """
            Deleted transaction for acount
         """
        get_object_or_404(Account, id=id_acount)

        serializer = TransactionDeleteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "code": 400,
                    "message": "The request is not valid",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        get_object_or_404(Transaction, id=serializer.initial_data['id'])
        Transaction.objects.filter(id=serializer.initial_data['id']).delete()
        return Response(
            {
                "success": True,
                "code": 200,
                "message": "Transation was delete"
            },
            status=status.HTTP_200_OK
        )


class TransactionInterAcountView(APIView):

    def post(self, request):
        """
        Creates new acount
        """
        data = request.data
        get_object_or_404(Account, id=data['from']['id'])
        get_object_or_404(Account, id=data['to']['id'])
        # from
        amount = data['from']['balance']

        keyword_from = {
            "amount": amount,
            "description": "movimiento entre cuentas",
            "income": False,
            "accounts_id": data['from']['id']
        }
        crear_transaccion(**keyword_from)

        Account.objects.filter(id=data['from']['id']).update(balance=F('balance') - amount)

        # to
        keyword_to = {
            "amount": amount,
            "description": "movimiento entre cuentas",
            "income": True,
            "accounts_id": data['to']['id']
        }
        crear_transaccion(**keyword_to)

        Account.objects.filter(id=data['to']['id']).update(balance=F('balance') + amount)
        return Response(
            {
                "success": True,
                "code": 200,
                "message": "Transation done"
            },
            status=status.HTTP_200_OK
        )