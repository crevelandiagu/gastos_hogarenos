from .models import Account
from .models import Transaction

def crear_transaccion(**keyword):

    create_transaction = Transaction(
        amount=keyword['amount'],
        description=keyword["description"],
        income=keyword["income"],
        accounts_id=keyword['accounts_id']
    )
    create_transaction.save()

def crear_acount():
    pass