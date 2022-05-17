from django.contrib import admin

from .models import (
    Article, ArticleCategory, ArticlePhoto, Catalog, CatalogCategory,
    Certificate,
)


class ArticlePhotoInlineAdmin(admin.StackedInline):
    model = ArticlePhoto
    extra = 0
    min_num = 0
    ordering = ('created_at',)
    raw_id_fields = ('photo',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ('created_at',)
    raw_id_fields = ('photo',)
    inlines = [ArticlePhotoInlineAdmin]


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    ordering = ('created_at',)
    fields = ('ordering_num', 'slug', 'category', 'name', 'description', 'photo', 'file')
    list_display = ('name', 'ordering_num', 'category', 'created_at')
    list_filter = ('category',)
    raw_id_fields = ('photo', 'file')


@admin.register(CatalogCategory)
class CatalogCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    raw_id_fields = ('photo', 'file')
