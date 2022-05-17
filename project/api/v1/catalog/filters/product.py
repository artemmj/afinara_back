from django.db.models import Q

from django_filters import FilterSet, CharFilter


class ProductFilterSet(FilterSet):
    catalog = CharFilter(method='catalog_filter')
    catalog_parent = CharFilter(method='catalog_parent_filter')

    def catalog_filter(self, queryset, name, value):
        return queryset.filter(catalog__slug=value).distinct()

    def catalog_parent_filter(self, queryset, name, value):
        return queryset.filter(Q(catalog__parent__slug=value) | Q(catalog__slug=value)).distinct()
