import logging

from django.db.models.query import QuerySet
from rest_framework.exceptions import NotFound

from apps.catalog.models import Catalog
from .services import AttributeFilter

logger = logging.getLogger('django_info')


def sort_or_display_queryset(query_params: dict, queryset: QuerySet) -> QuerySet:
    """ Функция решает, в зависимости от параметров запроса, какая страница
    нужна фронту. При первом попадании на первые страницы списков товаров
    необходимо отобразить первыми товары, отмеченные флагом в админке.
    """
    query_params.pop('per_page', None)

    if len(query_params) == 0:
        queryset = queryset.order_by('-display_in_top_wo_catalog')
    elif 'catalog' in query_params and len(query_params) <= 1:
        try:
            catalog = Catalog.objects.get(slug=query_params['catalog'])
        except Catalog.DoesNotExist:
            raise NotFound(f'Каталог ({query_params["catalog"]}) не существует.')
        if catalog.parent:
            queryset = queryset.order_by('-display_in_top_in_child')
        else:
            queryset = queryset.order_by('-display_in_top_in_parent')
    elif 'ordering' in query_params:
        queryset = queryset
    else:
        queryset = AttributeFilter(query_params).filter_queryset(queryset)

    return queryset
