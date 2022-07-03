from django.contrib import admin
from .models import Transaction

# Register your models here.


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ("description", "type", "amount", "date")
    ordering = ("-date",)
    list_per_page = 20


admin.site.register(Transaction, TransactionsAdmin)
