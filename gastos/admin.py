from django.contrib import admin
from .models import Account
from .models import Transaction

class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount', 'description', 'income']


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
