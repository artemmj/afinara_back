from django_filters import FilterSet, CharFilter, BooleanFilter


class CatalogFilterSet(FilterSet):
    root = BooleanFilter(field_name='parent', lookup_expr='isnull')
    parent = CharFilter(field_name='parent__slug')
