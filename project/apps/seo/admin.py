from django.contrib import admin

from .models import Seo


@admin.register(Seo)
class SeoAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'route', 'title', 'h1', 'description', 'keywords', 'canonical_rel',
    )
