from functools import lru_cache
from typing import Optional

from django.db.models import Subquery, Max, Min, Q
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from api.v1.catalog.filters import ProductFilterSet
from apps.helpers.serializers import EnumField, EagerLoadingSerializerMixin
from apps.catalog.models import Filter, ProdAttr, Product, Attribute


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ('id', 'slug', 'name')


class ParentFilterSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()

    class Meta:
        model = Filter
        fields = ('attribute',)


class FilterSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    type = EnumField(enum_class=Filter.Type)
    min = serializers.SerializerMethodField(help_text='возвращается для типа range', required=False)
    max = serializers.SerializerMethodField(help_text='возвращается для типа range', required=False)
    choices = serializers.SerializerMethodField(help_text='возвращается для типа choice и multi_choice', required=False)
    attribute = AttributeSerializer()
    available = serializers.SerializerMethodField(required=False)
    parent = ParentFilterSerializer()

    select_related_fields = ['attribute']

    class Meta:
        model = Filter
        fields = (
            'id', 'name', 'type', 'min', 'max', 'choices', 'attribute',
            'ordinal_number', 'available', 'parent'
        )

    @lru_cache()
    def _get_attributes(self, obj):
        params = self.context['request'].query_params.copy()
        products = ProductFilterSet(data=params, queryset=Product.objects.all()).qs.values('id')

        # Если у текущего обрабатываемого фильтра есть лимитирующий фильтр,
        # то дополнительно отфильтровать варианты по значению в params.
        if obj.limitation_filter:
            limit_slug = obj.limitation_filter.attribute.slug
            if limit_slug in params:
                products = products.filter(attributes__text_translit=params[limit_slug])

        return ProdAttr.objects.filter(
            product_id__in=Subquery(products.values('id')),
            attribute_id=obj.attribute_id
        )

    def get_min(self, obj) -> Optional[float]:
        if obj.type != Filter.Type.RANGE:
            return

        return self._get_attributes(obj).aggregate(res=Min('numeric'))['res'] or 0.0

    def get_max(self, obj) -> Optional[float]:
        if obj.type != Filter.Type.RANGE:
            return

        return self._get_attributes(obj).aggregate(res=Max('numeric'))['res'] or 0.0

    @swagger_serializer_method(serializer_or_field=serializers.ListField(child=serializers.CharField()))
    def get_choices(self, obj):
        if obj.type not in [Filter.Type.CHOICE, Filter.Type.MULTI_CHOICE]:
            return

        attrs = self._get_attributes(obj).values_list('text', 'text_translit', flat=False).distinct()
        # Сначала, список атрибутов разделить на два - которые можно
        # привести к флоат, и которые нет. Для неимеющих десятичной части
        # чисел, необходимо убрать десятичный ноль .0
        digit_list, char_list = list(), list()
        for attr in attrs:
            try:
                digitval_one = float(attr[0])
                digitval_two = float(attr[1])
                digit_list.append([digitval_one, digitval_two])
            except ValueError:
                char_list.append(attr)

        without_zeros_digits = list()
        for digit in sorted(digit_list):
            without_zeros_digit = list()
            without_zeros_digit.append('%g' % digit[0])
            without_zeros_digit.append('%g' % digit[1])
            without_zeros_digits.append(without_zeros_digit)
        return list(map(lambda x: x, without_zeros_digits)) + sorted(char_list)

    def get_available(self, obj) -> bool:
        """ Решить, является ли запрос 'корневым', или есть параметры,
        которые надо проверить на доступность для выбора.
        """
        if not obj.parent:
            return True

        params = self.context['request'].query_params.copy()
        params.pop('catalog', None)
        params.pop('root', None)

        if obj.parent.attribute.slug in params:
            values = params[obj.parent.attribute.slug].split(',')
            return obj.parent_value in values
        return False
