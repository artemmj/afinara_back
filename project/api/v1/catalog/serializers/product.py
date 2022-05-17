from typing import Optional

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.catalog.models import Product, SizeChart
from api.v1.file.serializers import FileSerializer

from .catalog import CatalogNameSerializer
from apps.support.models import Catalog as SupportCatalog
from apps.catalog.models import ProdAttr


def float_to_int(obj):
    if obj:
        try:
            return int(float(obj.text))
        except Exception:
            return obj.text
    return None


class ProductSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    catalog = CatalogNameSerializer()
    catalog_parent = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    #select_related_fields = ['catalog__parent']
    #prefetch_related_fields = ['photos']

    class Meta:
        model = Product
        fields = (
            'id',
            'created_at',
            'vendor_code',
            'name',
            'full_name',
            'price',
            'measure',
            'catalog',
            'catalog_parent',
            'photos',
        )

    @swagger_serializer_method(serializer_or_field=serializers.CharField())
    def get_name(self, obj):
        name = obj.name

        if diameters := obj.attributes.filter(attribute__name='Диаметр'):
            try:
                if diameters[0].text[0].isnumeric():
                    name += f' d{int(float(diameters[0].text))}'
                else:
                    name += f' {int(float(diameters[0].text))}'
            except Exception:
                name += f' {diameters[0].text}'

        if pressures := obj.attributes.filter(attribute__name='SDR - давление'):
            name += f' {pressures[0].text}'

        if performance := obj.attributes.filter(attribute__name='Производительность, м3/ч'):
            name += f' {int(float(performance[0].text))} м3/ч'

        return name

    @swagger_serializer_method(serializer_or_field=CatalogNameSerializer)
    def get_catalog_parent(self, obj):
        return CatalogNameSerializer(obj.catalog.parent).data if obj.catalog.parent else None

    @swagger_serializer_method(serializer_or_field=FileSerializer(many=True))
    def get_photos(self, obj):
        serializer = FileSerializer(obj.photos.order_by('created_at'), many=True, context=self.context)
        return serializer.data


class ProductDetailDescriptionSerializer(serializers.Serializer):
    material = serializers.CharField()
    color = serializers.CharField()
    pressure = serializers.CharField()
    temperature = serializers.CharField()
    diameters = serializers.CharField()
    text = serializers.CharField()
    expand = serializers.CharField()
    seal_material = serializers.CharField(required=False)
    membrane_material = serializers.CharField(required=False)
    scale = serializers.CharField(required=False)


class RawDataSerializer(serializers.Serializer):
    material = serializers.CharField()
    color = serializers.CharField(default=None)
    temperature = serializers.CharField(default=None)
    text = serializers.CharField(source='description_text')

    diameters = serializers.SerializerMethodField()
    seal_material = serializers.SerializerMethodField(required=False)
    pressure = serializers.SerializerMethodField()
    expand = serializers.SerializerMethodField(required=False)
    membrane_material = serializers.SerializerMethodField(required=False)
    scale = serializers.SerializerMethodField(required=False)
    wetted_materials = serializers.SerializerMethodField()
    tolerance_diameters = serializers.SerializerMethodField()
    configuration = serializers.SerializerMethodField()
    spring_material = serializers.SerializerMethodField()

    def get_diameters(self, obj) -> Optional[str]:
        return float_to_int(obj.attributes.filter(attribute__name='Диаметр').first())

    def get_seal_material(self, obj) -> Optional[str]:
        if seal_material := obj.attributes.filter(attribute__name='Материал уплотнения').first():
            return seal_material.text

    def get_pressure(self, obj) -> Optional[str]:
        if pressures := obj.attributes.filter(attribute__name='SDR - давление').first():
            return pressures.text

    def get_expand(self, obj) -> Optional[str]:
        return float_to_int(obj.attributes.filter(attribute__name='Расход').first())

    def get_membrane_material(self, obj) -> Optional[str]:
        if membran_material := obj.attributes.filter(attribute__name='Материал мембраны').first():
            return membran_material.text

    def get_scale(self, obj) -> Optional[str]:
        if scale := obj.attributes.filter(attribute__name='Шкала').first():
            return scale.text

    def get_wetted_materials(self, obj) -> Optional[str]:
        if wett_materials := obj.attributes.filter(attribute__name='Смачиваемые материалы').first():
            return wett_materials.text

    def get_tolerance_diameters(self, obj) -> Optional[str]:
        if toler_diametr := obj.attributes.filter(attribute__name='Допуск на диаметр (мм)').first():
            return toler_diametr.text

    def get_configuration(self, obj) -> Optional[str]:
        if config := obj.attributes.filter(attribute__name='Конфигурация').first():
            return config.text

    def get_spring_material(self, obj) -> Optional[str]:
        if spring_material := obj.attributes.filter(attribute__name='Материал пружины').first():
            return spring_material.text
        elif spring_material := obj.attributes.filter(attribute__name='Материал пружины ').first():
            return spring_material.text


class ProductDetailAssortmentSerializer(serializers.ModelSerializer):
    diameter = serializers.SerializerMethodField()
    expand = serializers.SerializerMethodField(required=False)
    seal_material = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'diameter',
            'expand',
            'vendor_code',
            'price',
            'seal_material',
        )

    def get_expand(self, obj) -> str:
        return float_to_int(obj.attributes.filter(attribute__name='Расход').first())

    def get_diameter(self, obj) -> str:
        return float_to_int(obj.attributes.filter(attribute__name='Диаметр').first())

    def get_seal_material(self, obj) -> str:
        if obj.catalog.name in ['Приводная арматура', 'Запорная арматура']:
            attr = obj.attributes.filter(attribute__name='Материал уплотнения').first()
            if attr:
                return attr.text
        return None


class IntSupportCatalogSerializer(serializers.ModelSerializer):
    photo = FileSerializer()
    file = FileSerializer()

    class Meta:
        model = SupportCatalog
        fields = (
            'id',
            'name',
            'description',
            'photo',
            'file',
        )
        read_only_fields = ('id', 'created_at',)


class ProductDetailSizeChartSerializer(serializers.ModelSerializer):
    class SizeChartSerializer(serializers.ModelSerializer):
        class Meta:
            model = SizeChart
            fields = (
                'id',
                'title',
                'value',
            )

    size_chart = SizeChartSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'vendor_code',
            'size_chart',
        )


class ProductDetailSerializer(ProductSerializer, serializers.ModelSerializer):
    assortment = serializers.SerializerMethodField()
    description = RawDataSerializer(source='*')
    size_chart = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            *ProductSerializer.Meta.fields, 'description', 'assortment', 'size_chart', 'files'
        )

    @swagger_serializer_method(serializer_or_field=ProductDetailAssortmentSerializer(many=True))
    def get_assortment(self, obj):
        products = Product.objects.filter(name=obj.name, catalog=obj.catalog)
        unordered_data = ProductDetailAssortmentSerializer(products, many=True).data
        try:
            return sorted(unordered_data, key=lambda product: product['diameter'])
        except Exception:
            return unordered_data

    @swagger_serializer_method(serializer_or_field=ProductDetailSizeChartSerializer(many=True))
    def get_size_chart(self, obj):
        products = Product.objects.filter(name=obj.name, catalog=obj.catalog)
        unordered_data = ProductDetailSizeChartSerializer(products, many=True).data
        return unordered_data

    def get_files(self, obj) -> str:
        support_catalogs = obj.support_catalogs.all()
        serializer = IntSupportCatalogSerializer(support_catalogs, many=True, context=self.context)
        return serializer.data

    @swagger_serializer_method(serializer_or_field=serializers.CharField())
    def get_name(self, obj):
        name = obj.name
        prodattrs = ProdAttr.objects.filter(product=obj)
        for prodattr in prodattrs:
            if prodattr.attribute.name == 'Диаметр':
                try:
                    int_value = int(float(prodattr.text))
                    name += f' d{int_value}'
                except Exception:
                    name += f' {prodattr.text}'
            if prodattr.attribute.name == 'SDR - давление':
                name += f' {prodattr.text}'
            if prodattr.attribute.name == 'Производительность, м3/ч':
                name += f' {prodattr.text} м3/ч'
        return name


class ProductPrintAssortmentSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=True)


class ProductPrintAssortmentResponseSerializer(serializers.Serializer):
    file = serializers.CharField()


class ProductPrintSizeChartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=True)


class ProductPrintSizeChartResponseSerializer(serializers.Serializer):
    file = serializers.CharField()
