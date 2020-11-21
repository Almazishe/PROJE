from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = (
        'email',
        'is_staff',
        'created_at'
    )

    readonly_fields = (
        'uuid', 
        'created_at', 
        'updated_at', 
        'last_login', 
    )

    ordering = (
        'created_at',
    )