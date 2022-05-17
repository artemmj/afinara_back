from django_filters import FilterSet, CharFilter, Filter


class TableOfChemicalResistanceFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    state = CharFilter(field_name='state')
    formula = CharFilter(field_name='formula')
    concentration = CharFilter(field_name='concentration')
    temperature = Filter('temperature')
