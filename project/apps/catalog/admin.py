import os

from django.contrib import admin
from django.utils.html import format_html
from django.conf.urls import url
from django.urls import reverse
from django.conf import settings
from django import forms

from .models import Catalog, Product, Attribute, Filter, ProdAttr, SizeChart
from .tasks import load_catalog_assortment

from django.shortcuts import render
from rest_framework.exceptions import MethodNotAllowed
from .forms import LoadAssortmentForm


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    fields = ('show_on_mainpage', 'ordering_num', 'name', 'slug', 'parent', 'photo', 'description',)
    list_display = ('__str__', 'load_assortment_action', 'name', 'ordering_num', 'created_at',)
    raw_id_fields = ('photo',)
    ordering = ('-created_at',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<catalog_id>.+)/loadassortment/$',
                self.admin_site.admin_view(self.load_assortment),
                name='load-assortment',
            ),
            url(
                r'/load-successfully-started/',
                self.admin_site.admin_view(self.load_successfully_started),
                name='load-successfully-started',
            )
        ]
        return custom_urls + urls

    def load_assortment_action(self, obj):
        if not obj.parent:
            return format_html(
                '<a class="button" href="{}">Загрузить</a>',
                reverse('admin:load-assortment', args=[obj.pk]),
            )
        else:
            return

    load_assortment_action.short_description = 'Загрузить ассортимент'
    load_assortment_action.allow_tags = True

    def check_price_images_files(self, request) -> dict:
        args = dict()
        if 'price_files' in request.FILES:
            dest = f'{settings.MEDIA_ROOT}/assortment'
            files = request.FILES.getlist('price_files')
            filedests = list()
            for f in files:
                filedest = f'{dest}/цены_{f.name}'
                with open(filedest, 'wb+') as fout:
                    for chunk in f.chunks():
                        fout.write(chunk)
                filedests.append(filedest)
            args['price_files'] = filedests
        if 'images_file' in request.FILES:
            dest = f'{settings.MEDIA_ROOT}/assortment/{request.FILES["images_file"].name}'
            with open(dest, 'wb+') as fout:
                for chunk in request.FILES['images_file'].chunks():
                    fout.write(chunk)
            args['images_file'] = dest
        return args

    def load_assortment(self, request, catalog_id, *args, **kwargs):
        if request.method == 'GET':
            form = LoadAssortmentForm()
        elif request.method == 'POST':
            form = LoadAssortmentForm(request.POST, request.FILES)
            if form.is_valid():
                if not os.path.exists(f'{settings.MEDIA_ROOT}/assortment'):
                    os.mkdir(f'{settings.MEDIA_ROOT}/assortment')
                dest = f'{settings.MEDIA_ROOT}/assortment/{request.FILES["assortment_file"].name}'
                with open(dest, 'wb+') as fout:
                    for chunk in request.FILES['assortment_file'].chunks():
                        fout.write(chunk)

                # Проверить наличие файлов цен и архива картинок
                args = self.check_price_images_files(request)
                task_id = load_catalog_assortment.delay(dest, catalog_id, **args)

                return render(
                    request,
                    'catalog/load_success_start.html',
                    {
                        'task_id': task_id,
                    },
                )
        else:
            raise MethodNotAllowed()

        return render(
            request,
            'catalog/load_assortment.html',
            {
                'form': form,
                'catalog_id': catalog_id,
            },
        )

    def load_successfully_started(self, request, *args, **kwargs):
        if request.method == 'GET':
            return render(request, 'catalog/load_success_start.html')
        else:
            raise MethodNotAllowed()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class ProductPhotoInline(admin.StackedInline):
        model = Product.photos.through
        extra = 0
        min_num = 0
        raw_id_fields = ('file',)

    class ProductSizeChartInline(admin.TabularInline):
        model = SizeChart
        extra = 0
        min_num = 0

    list_display = (
        'vendor_code',
        'name',
        'full_name',
        'price',
        'measure',
        'catalog',
        'created_at',
    )
    fields = (
        'display_in_top_wo_catalog',
        'display_in_top_in_parent',
        'display_in_top_in_child',
        'vendor_code',
        'name',
        'full_name',
        'price',
        'measure',
        'catalog',
        'support_catalogs',
    )
    search_fields = ('vendor_code',)
    list_filter = ('catalog',)
    raw_id_fields = ('support_catalogs',)
    inlines = [ProductPhotoInline, ProductSizeChartInline]
    ordering = ('-created_at',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('name', 'type',)
    fields = ('name', 'type',)


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ('name', 'catalog', 'attribute', 'type', 'ordinal_number', 'parent', 'parent_value')


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('ordinal_number', '__str__', 'attribute', 'type', 'catalog',)
    fields = (
        'name', 'catalog', 'attribute', 'type', 'ordinal_number', 'parent',
        'parent_value', 'limitation_filter',
    )
    list_display_links = ('ordinal_number', '__str__',)
    list_filter = ('catalog',)
    ordering = ('-created_at',)
    form = FilterForm


@admin.register(ProdAttr)
class ProdAttrAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'numeric', 'text', 'text_translit')
    ordering = ('-created_at',)
