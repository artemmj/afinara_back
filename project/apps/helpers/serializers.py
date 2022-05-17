from drf_yasg import openapi
from rest_framework import serializers


class EagerLoadingSerializerMixin:

    select_related_fields = []
    prefetch_related_fields = []

    @classmethod
    def setup_eager_loading(cls, queryset):
        if cls.select_related_fields:
            queryset = queryset.select_related(*cls.select_related_fields)
        if cls.prefetch_related_fields:
            queryset = queryset.prefetch_related(*cls.prefetch_related_fields)
        return queryset


class EmptySerializer(serializers.Serializer):
    pass


class DeleteBatchRequestSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.UUIDField())


class DeleteBatchSerializer(serializers.Serializer):
    def get_fields(self):
        fields = super().get_fields()
        fields['items'] = serializers.PrimaryKeyRelatedField(queryset=self.context['queryset'], many=True)
        return fields


class EnumSerializer(serializers.Serializer):
    value = serializers.CharField()
    name = serializers.CharField(source='label')


class EnumField(serializers.Field):
    enum_class = None
    ref_name = None

    class Meta:
        pass

    def __init__(self, enum_class=None, ref_name=None, *args, **kwargs):
        self.enum_class = enum_class or self.enum_class
        self.Meta.swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": ref_name or self.ref_name or self.enum_class.__name__,
            "properties": {
                "name": openapi.Schema(
                    title="Название",
                    type=openapi.TYPE_STRING,
                    enum=self.enum_class.labels,
                ),
                "value": openapi.Schema(
                    title="Значение",
                    type=openapi.TYPE_STRING,
                    enum=self.enum_class.values,
                ),
            },
        }
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if data not in self.enum_class.values:
            self.fail('invalid_choice', input=data)

        return data

    def to_representation(self, value):
        return EnumSerializer(self.enum_class[value.upper()]).data if value else None


class FixAbsolutePathCkEditorSerializer(serializers.Field):
    """
    Сериализатор подменяет относительный путь до изображения
    на абсолютный для картинок creditor.
    """
    SEARCH_PATTERN_SRC = 'src=\"/media/ckeditor_uploads/'

    def to_representation(self, value):
        request = self.context.get("request")
        site_domain = request.get_host()
        replaced = 'src=\"%s/media/ckeditor_uploads/' % site_domain
        text = value.replace(self.SEARCH_PATTERN_SRC, replaced)
        return text
