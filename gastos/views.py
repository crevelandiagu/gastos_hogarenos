import os
import json

from .models import Account
from .models import Transaction

from .serializers import AccountSerializer
from .serializers import AccountDetailSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class Health(APIView):
    """Check avaiability"""

    def get(self, request):
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class AccountView(APIView):

    def post(self, request):
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
        return Response(
            {
                "success": True,
                "code": 200,
                "account": {
                    "name": serializer.data['name'],
                    "balance": serializer.data['balance']
                },
            },
            status=status.HTTP_200_OK
        )

    def get(self, request):
        """
        get acount's
        """
        documents = Account.objects.all()
        serializer = AccountSerializer(documents, many=True)
        return Response(serializer.data)


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
