from django_filters import FilterSet, CharFilter, BooleanFilter


class FilterFilterSet(FilterSet):
    catalog = CharFilter(field_name='catalog__slug')
    root = BooleanFilter(field_name='catalog', lookup_expr='isnull')
