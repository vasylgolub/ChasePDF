from django.contrib import admin

# Register your models here.
from .models import BankStatement, ListOfStatementFiles

admin.site.register(BankStatement)
admin.site.register(ListOfStatementFiles)