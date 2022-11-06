from django.contrib import admin

# Register your models here.
from .models import Transaction, Statement

admin.site.register(Transaction)
admin.site.register(Statement)