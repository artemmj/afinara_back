from django.contrib import admin

from .models import MailRecipient


@admin.register(MailRecipient)
class MailRecipientAdmin(admin.ModelAdmin):
    pass
