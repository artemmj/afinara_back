import logging

from apps.catalog.models import Attribute

logger = logging.getLogger('django_info')


class AttributeFilter:
    exclude_filters = {'page', 'per_page', 'catalog', 'search', 'ordering'}

    def __init__(self, params, exclude_filters=None):
        self.exclude_filters = exclude_filters or self.exclude_filters
        self.params = params
        self.attribute_slugs = set(params.keys()) - self.exclude_filters

    def get_filter(self, attribute_slug):
        attribute = Attribute.objects.get(slug=attribute_slug)

        filters = {'attributes__attribute': attribute}
        params = self.params[attribute_slug].split(',')

        if attribute.type == Attribute.AttrTypes.CHAR:
            # Перед фильтрацией по атрибутам стоит знать, что числовые
            # типы, даже в символьном варианте, лежат в БД в формате как
            # с десятичной точкой, так и просто интом. Следовательно,
            # перед фильтрацией надо попытаться привести к float и int,
            # затем к str.
            correct_params = list()
            for param in params:
                try:
                    correct_params.append(str(float(param)))
                    correct_params.append(str(int(param)))
                except ValueError:
                    correct_params.append(param)
                except Exception as exc:
                    raise ValueError(f'Возникла ошибка при конвертации параметров фильтра / {exc}')

            filters['attributes__text_translit__in'] = correct_params
        else:
            filters['attributes__numeric__gte'] = float(params[0])
            filters['attributes__numeric__lte'] = float(params[1])
        return filters

    def filter_queryset(self, queryset):
        for attribute_slug in self.attribute_slugs:
            try:
                queryset = queryset.filter(**self.get_filter(attribute_slug))
            except Exception as e:
                logger.info(f'bad product filter {attribute_slug}={self.params[attribute_slug]} - {e}')

        return queryset
