from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('id', 'file', 'created_at')
