import os
import json

from .models import Account
from .models import Transaction

from .serializers import AccountSerializer
from .serializers import AccountDetailSerializer
from .serializers import TransactionSerializer
from .serializers import TransactionDeleteSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404

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

        create_transaction = Transaction(
            amount=serializer.data['balance'],
            description="balance inicia",
            income=True,
            accounts_id=create_account.id
        )
        create_transaction.save()

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

        create_transaction = Transaction(
            amount=serializer.data['balance'],
            description="ajuste manual",
            income=True,
            accounts_id=id_acount
        )
        create_transaction.save()

        return Response(
            {
                "success": True,
                "code": 200,
                "account": id_acount,
            },
            status=status.HTTP_200_OK
        )


class AccountDetailView(APIView):

    def get(self, request, id):
        """
        get details acount's
        """

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
        create_transaction = Transaction(
            amount=serializer.data['amount'],
            description=serializer.data['description'],
            income=serializer.data['income'],
            accounts_id=id_acount
        )
        create_transaction.save()

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