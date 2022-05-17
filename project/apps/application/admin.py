from django.contrib import admin
from apps.application.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search = ('name', 'phone')
    list_filter = ('name',)
    raw_id_fields = ('files',)
