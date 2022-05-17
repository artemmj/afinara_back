from django_filters import FilterSet, CharFilter


class ArticleFilterSet(FilterSet):
    category = CharFilter(field_name='category__slug')


class CatalogFilterSet(FilterSet):
    category = CharFilter(field_name='category__slug')
